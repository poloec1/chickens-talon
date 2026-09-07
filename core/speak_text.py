"""Read text out loud with the macOS `say` command.

Use case: hear a Claude (or any) response read aloud — select the text and say
"speak this", or say "speak clip" to read whatever is on the clipboard.

`say` runs in a background process so speech never blocks Talon; "stop speaking"
terminates the current utterance.
"""

import subprocess

from talon import Module, actions

mod = Module()

_proc: subprocess.Popen | None = None


def _speak(text: str):
    global _proc
    text = (text or "").strip()
    if not text:
        return
    _stop()
    # Feed text on stdin so long responses aren't capped by arg length.
    _proc = subprocess.Popen(["say", "-f", "-"], stdin=subprocess.PIPE)
    _proc.stdin.write(text.encode("utf-8"))
    _proc.stdin.close()


def _stop():
    global _proc
    if _proc and _proc.poll() is None:
        _proc.terminate()
    _proc = None


@mod.action_class
class Actions:
    def speak_selection():
        """Read the currently selected text aloud."""
        _speak(actions.edit.selected_text())

    def speak_clipboard():
        """Read the current clipboard text aloud."""
        _speak(actions.clip.text())

    def speak_stop():
        """Stop any in-progress speech."""
        _stop()
