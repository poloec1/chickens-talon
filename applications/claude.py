"""Press the "Read aloud" button on the most recent Claude response in the
Claude desktop app.

The button has no keyboard shortcut and its screen position varies, so we drive
it through macOS accessibility (AX): find the bottom-most button whose label
looks like a read-aloud control and AXPress it.

Claude desktop is Electron/Chromium, which hides its web-content AX tree unless
`AXManualAccessibility` is set on the app — so we set that first, then search.

If the main command does nothing, say "read aloud debug": it logs every button
label the AX tree exposes to the Talon log, so the real label can be confirmed.
"""

from talon import Module, actions, app, ui

mod = Module()

BUNDLE = "com.anthropic.claudefordesktop"

# Substrings (lower-case) that identify the read-aloud / play control. Kept
# tight to avoid pressing unrelated buttons; extend after checking "read aloud
# debug" if the real label differs.
LABEL_PATTERNS = ("read aloud", "read this", "read message", "listen aloud")

# The always-present control that reveals a message's collapsed action row.
# Pressed first (hands-free) so the read-aloud toggle renders into the AX tree
# without needing a mouse hover.
REVEAL_PATTERNS = ("show message actions",)

MAX_NODES = 12000


def _claude_app():
    apps = ui.apps(bundle=BUNDLE, background=False)
    return apps[0] if apps else None


def _enable_ax(pid: int):
    """Force Chromium/Electron to expose its web-content AX tree."""
    try:
        from ApplicationServices import (
            AXUIElementCreateApplication,
            AXUIElementSetAttributeValue,
        )

        ref = AXUIElementCreateApplication(pid)
        AXUIElementSetAttributeValue(ref, "AXManualAccessibility", True)
    except Exception as e:
        print("claude read-aloud: could not set AXManualAccessibility:", e)


def _walk(root):
    # Pre-order DFS that preserves document order (push children reversed so
    # pop() yields them left-to-right), so the last match == most recent message.
    stack = [root]
    seen = 0
    while stack and seen < MAX_NODES:
        el = stack.pop()
        seen += 1
        yield el
        try:
            stack.extend(reversed(el.children))
        except Exception:
            pass


def _describe(el):
    try:
        d = el.dump()
    except Exception:
        return "", ""
    role = str(d.get("AXRole", "") or "")
    parts = []
    for k in ("AXDescription", "AXTitle", "AXRoleDescription", "AXHelp", "AXValue"):
        v = d.get(k)
        if isinstance(v, str) and v:
            parts.append(v)
    return role, " ".join(parts).lower()


def _bottom(el):
    try:
        return el.rect.y
    except Exception:
        return -1.0


def _pressable(el):
    # Role-agnostic: the read-aloud control is an AXCheckBox, not a button, so
    # match on whether the element actually supports AXPress rather than on role.
    try:
        return "AXPress" in (el.actions or [])
    except Exception:
        return False


def _root():
    """Return (app, active-window root element) with AX forced on, or (None, None)."""
    a = _claude_app()
    if not a:
        app.notify("Claude", "Desktop app not running")
        return None, None
    _enable_ax(a.pid)
    try:
        return a, a.active_window.element
    except Exception:
        app.notify("Claude", "No active window")
        return None, None


def _collect(root, patterns):
    """All pressable elements whose label matches, in document order."""
    out = []
    for el in _walk(root):
        _role, label = _describe(el)
        if any(p in label for p in patterns) and _pressable(el):
            out.append(el)
    return out


def _axvalue(el):
    try:
        return el.dump().get("AXValue")
    except Exception:
        return "?"


def _press(el) -> bool:
    try:
        el.perform("AXScrollToVisible")
    except Exception:
        pass
    try:
        el.perform("AXPress")
        print(f"  pressed AXValue-was={_axvalue(el)!r}")
        return True
    except Exception as e:
        print("claude read-aloud: AXPress failed:", e)
        return False


def _press_latest_matching(root, patterns) -> bool:
    # Web AX reports no usable geometry (y=-1), so use document order: the last
    # match belongs to the most recent message.
    matches = _collect(root, patterns)
    print(f"  matches for {patterns}: {len(matches)} -> "
          f"values={[_axvalue(m) for m in matches]}")
    return _press(matches[-1]) if matches else False


@mod.action_class
class Actions:
    def claude_read_latest():
        """Read the most recent Claude response aloud — hands-free.

        Fast path: press the toggle if it's already in the tree. Otherwise
        reveal the latest message's action row first, then press it.
        """
        a, root = _root()
        if not root:
            return
        print("=== claude read-aloud invoke ===")
        print(" fast path:")
        if _press_latest_matching(root, LABEL_PATTERNS):
            return
        # Not visible yet: reveal the latest message's actions, then retry.
        print(" reveal path:")
        if _press_latest_matching(root, REVEAL_PATTERNS):
            actions.sleep("400ms")
            _, root = _root()
            print(" post-reveal retry:")
            if root and _press_latest_matching(root, LABEL_PATTERNS):
                return
        app.notify("Claude", "No read-aloud toggle found (see log)")
        print("claude read-aloud: no match — run 'read aloud debug' to inspect")

    def claude_stop_aloud():
        """Toggle off read-aloud on the most recent response (same toggle control)."""
        actions.user.claude_read_latest()

    def claude_read_probe():
        """Log the read-aloud matches with their AXValue and actions (state probe)."""
        a, root = _root()
        if not root:
            return
        n = 0
        print("=== claude read-aloud probe ===")
        for el in _walk(root):
            _role, label = _describe(el)
            if not any(p in label for p in LABEL_PATTERNS):
                continue
            try:
                d = el.dump()
            except Exception:
                d = {}
            try:
                acts = list(el.actions or [])
            except Exception:
                acts = "?"
            n += 1
            print(
                f"[{d.get('AXRole')}] label={label!r} "
                f"AXValue={d.get('AXValue')!r} "
                f"AXFocused={d.get('AXFocused')!r} actions={acts}"
            )
        print(f"=== {n} read-aloud matches ===")
        app.notify("Claude", f"{n} read-aloud matches probed (see log)")

    def claude_read_debug():
        """Log every button label in the Claude AX tree, to confirm the real one.

        Reveals the latest message's action row first, so controls that only
        render when the row is open (e.g. the playing-state stop control) are
        captured too.
        """
        a, root = _root()
        if not root:
            return
        if _press_latest_matching(root, REVEAL_PATTERNS):
            actions.sleep("400ms")
            _, root = _root()
            if not root:
                return

        count = 0
        hits = 0
        audio_kw = ("aloud", "speak", "listen", "audio", "play", "voice",
                    "sound", "tts", "narrat", "read out")
        print("=== claude read-aloud debug: button-like elements ===")
        for el in _walk(root):
            role, label = _describe(el)
            rl = role.lower()
            if "button" in rl:
                count += 1
                print(f"[{role}] y={_bottom(el):.0f} label={label!r}")
            # Also catch audio-ish controls of ANY role (image, menu item, etc.)
            if "button" not in rl and any(k in label for k in audio_kw):
                hits += 1
                print(f"AUDIO? [{role}] label={label!r}")
        print(f"=== {count} button-like elements, {hits} audio-keyword elements ===")
        app.notify("Claude", f"{count} buttons, {hits} audio hits (see log)")
