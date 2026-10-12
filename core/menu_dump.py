"""Walk the focused app's entire menu bar and dump every item + keyboard
shortcut to a JSON file, so a coding agent can generate voice commands from it.

Usage (voice): focus the target app, say "menu dump".
Output: /tmp/talon_app_menus.json

Key-conversion logic (modifier masks, virtual-key names) is ported from
talon_axkit/menu.py, which credits an Eric Schlegel email from 2004 as the only
documentation of the AXMenuItemCmd* accessibility attributes.
"""

import json

from talon import Module, app, ui

mod = Module()

OUTPUT_PATH = "/tmp/talon_app_menus.json"

# Modifier masks from <HIToolbox/Menus.h>
kMenuShiftModifier = 1 << 0
kMenuOptionModifier = 1 << 1
kMenuControlModifier = 1 << 2
kMenuNoCommandModifier = 1 << 3
kMenuFnGlobeModifier = 1 << 4

# Virtual key codes -> Talon key names (layout-independent keys only)
VK_NAMES = {
    0x24: "enter", 0x30: "tab", 0x31: "space", 0x33: "backspace", 0x35: "esc",
    0x73: "home", 0x74: "pageup", 0x75: "delete", 0x77: "end", 0x79: "pagedown",
    0x7B: "left", 0x7C: "right", 0x7D: "down", 0x7E: "up",
    0x7A: "f1", 0x78: "f2", 0x63: "f3", 0x76: "f4", 0x60: "f5", 0x61: "f6",
    0x62: "f7", 0x64: "f8", 0x65: "f9", 0x6D: "f10", 0x67: "f11", 0x6F: "f12",
}

MAX_DEPTH = 6


def menu_item_key(menu_item):
    """Return a Talon key string (e.g. 'cmd-shift-n') for an AXMenuItem, or None."""
    key_char = menu_item.get("AXMenuItemCmdChar")
    modifiers = menu_item.get("AXMenuItemCmdModifiers")
    virtual_key = menu_item.get("AXMenuItemCmdVirtualKey")

    key = None
    if key_char:
        key = key_char.lower()
    elif virtual_key is not None:
        key = VK_NAMES.get(virtual_key)
    if not key:
        return None

    keys = []
    if modifiers is not None:
        if not (modifiers & kMenuNoCommandModifier):
            keys.append("cmd")
        if modifiers & kMenuShiftModifier:
            keys.append("shift")
        if modifiers & kMenuOptionModifier:
            keys.append("alt")
        if modifiers & kMenuControlModifier:
            keys.append("ctrl")
        if modifiers & kMenuFnGlobeModifier:
            keys.append("fn")
    else:
        # No modifier info usually means no real shortcut; treat as none.
        return None

    keys.append(key)
    return "-".join(keys)


def submenu_of(element):
    """Return the AXMenu child of a menu / menu-bar item, or None."""
    try:
        return element.children.find_one(AXRole="AXMenu", max_depth=0)
    except ui.UIErr:
        return None


def walk(menu, path, out, depth):
    """Recurse an AXMenu, appending leaf items to out as {path, key, enabled}."""
    if depth > MAX_DEPTH:
        return
    try:
        children = menu.AXChildren
    except Exception:
        return
    for child in children:
        try:
            if child.AXRole != "AXMenuItem":
                continue
            title = child.get("AXTitle")
        except Exception:
            continue
        if not title:
            continue  # separator
        item_path = path + [title]
        submenu = submenu_of(child)
        if submenu is not None:
            walk(submenu, item_path, out, depth + 1)
        else:
            out.append(
                {
                    "path": item_path,
                    "key": menu_item_key(child),
                    "enabled": bool(child.get("AXEnabled")),
                }
            )


@mod.action_class
class Actions:
    def dump_app_menus():
        """Walk the active app's menu bar and write items+shortcuts to a JSON file."""
        active = ui.active_app()
        result = {"app_name": active.name, "bundle": active.bundle, "items": []}

        try:
            menu_bar = active.children.find_one(AXRole="AXMenuBar", max_depth=0)
        except ui.UIErr:
            app.notify("Menu dump failed", "No menu bar for the active app")
            return

        for bar_item in menu_bar.AXChildren:
            try:
                if bar_item.AXRole != "AXMenuBarItem":
                    continue
                title = bar_item.get("AXTitle")
            except Exception:
                continue
            if not title:
                continue
            submenu = submenu_of(bar_item)
            if submenu is not None:
                walk(submenu, [title], result["items"], 1)

        with open(OUTPUT_PATH, "w") as f:
            json.dump(result, f, indent=2)

        app.notify(
            "Menu dump complete",
            f'{active.name}: {len(result["items"])} items -> {OUTPUT_PATH}',
        )
