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

# Chromium/Electron roles a contenteditable chat composer typically maps to.
INPUT_ROLE_PATTERNS = ("textarea", "combobox", "textfield")

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
        if "AXPress" in (el.actions or []):
            return True
    except Exception:
        pass
    # Newer Claude builds no longer list AXPress in the actions of these
    # controls, but they still respond to it. Fall back to the role.
    try:
        return str(el.get("AXRole", "") or "") in ("AXButton", "AXCheckBox")
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


def _collect_text_inputs(root):
    # Document order, like _collect: the last match is whichever composer is
    # actually on screen (there's normally just one, but a modal could add more).
    out = []
    for el in _walk(root):
        try:
            role = str(el.get("AXRole", "") or "").lower()
        except Exception:
            continue
        if not any(p in role for p in INPUT_ROLE_PATTERNS):
            continue
        try:
            if "AXFocused" in (el.attrs or ()):
                out.append(el)
        except Exception:
            pass
    return out


def _collect(root, patterns):
    """All pressable elements whose label matches, in document order."""
    out = []
    for el in _walk(root):
        _role, label = _describe(el)
        # Match the control's own name (it is repeated as "<name> <name> button",
        # or "<name> for <message>"), not any text that merely mentions it, such
        # as session titles or suggestion buttons.
        if any(label.startswith(p + " " + p) or label.startswith(p + " for ")
               for p in patterns) and _pressable(el):
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
        try:
            print(f"  target rect={el.rect} actions={list(el.actions or [])}")
        except Exception as e:
            print("  target rect/actions unavailable:", e)
        el.perform("AXPress")
        print(f"  pressed AXValue-was={_axvalue(el)!r}")
        # The app ignores AXPress on this control, so the press alone does
        # nothing. It is scrolled into view; finish with the eye tracker.
        app.notify("Claude", "Look at the read aloud button and say click")
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

    def claude_read_last_message():
        """Read Claude's latest message aloud, ignoring any stale hover state.

        A message's action row, once revealed by hovering, stays in the AX
        tree after the mouse moves away. If an older message was hovered
        earlier, its still-revealed toggle beats a fresh one in the fast path
        used by claude_read_latest, so that command re-reads the old message
        instead of the new one. This command skips the fast path and always
        re-reveals the truly latest message's row first, so it can't be
        hijacked by a stale hover on an older message.
        """
        a, root = _root()
        if not root:
            return
        print("=== claude read last message ===")
        if not _press_latest_matching(root, REVEAL_PATTERNS):
            app.notify("Claude", "No message action row found (see log)")
            print("claude read last message: no reveal control — run 'read aloud debug' to inspect")
            return
        actions.sleep("400ms")
        _, root = _root()
        if root and _press_latest_matching(root, LABEL_PATTERNS):
            return
        app.notify("Claude", "No read-aloud toggle found after reveal (see log)")
        print("claude read last message: no match after reveal — run 'read aloud debug' to inspect")

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

    def claude_focus_chat_input():
        """Focus the session chat's text input box, hands-free.

        No menu item or shortcut exists for this, so we drive it through AX:
        find the composer's text-entry element (role AXTextArea/AXComboBox)
        and set its AXFocused attribute to True.
        """
        a, root = _root()
        if not root:
            return
        print("=== claude focus chat input ===")
        candidates = _collect_text_inputs(root)
        print(f"  candidates: {len(candidates)}")
        if not candidates:
            app.notify("Claude", "No chat input found (see log)")
            print("claude focus chat input: no match — run 'focus chat debug' to inspect")
            return
        el = candidates[-1]
        try:
            el.AXFocused = True
            print("  focused")
        except Exception as e:
            print("claude focus chat input: AXFocused set failed:", e)
            app.notify("Claude", "Could not focus chat input (see log)")

    def claude_focus_chat_input_debug():
        """Log every text-input-like element in the Claude AX tree (role, label, focused)."""
        a, root = _root()
        if not root:
            return
        print("=== claude focus chat input debug ===")
        n = 0
        for el in _walk(root):
            try:
                d = el.dump()
            except Exception:
                continue
            role = str(d.get("AXRole", "") or "")
            if not any(p in role.lower() for p in INPUT_ROLE_PATTERNS):
                continue
            n += 1
            print(
                f"[{role}] AXValue={d.get('AXValue')!r} "
                f"AXPlaceholderValue={d.get('AXPlaceholderValue')!r} "
                f"AXDescription={d.get('AXDescription')!r} "
                f"AXFocused={d.get('AXFocused')!r}"
            )
        print(f"=== {n} text-input-like elements ===")
        app.notify("Claude", f"{n} text inputs probed (see log)")

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
