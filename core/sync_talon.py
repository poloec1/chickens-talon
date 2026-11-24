"""Run the sync script that pulls the latest Talon repos, then show a notification.

Usage (voice): say "sync talon".
The script lives in the Talon user folder (sync-talon.sh).
"""

import os
import subprocess
import threading

from talon import Module, actions

mod = Module()

SCRIPT_PATH = os.path.expanduser("~/.talon/user/sync-talon.sh")


def _run():
    try:
        result = subprocess.run(
            ["/bin/bash", SCRIPT_PATH],
            capture_output=True,
            text=True,
            timeout=300,
        )
        failed = result.returncode != 0 or "fatal" in result.stdout.lower()
        message = "Talon sync finished with problems" if failed else "Talon sync finished"
    except Exception as error:
        message = f"Talon sync could not run: {error}"
    actions.app.notify(message)


@mod.action_class
class Actions:
    def sync_talon():
        """Pull the latest changes for the Talon repos in the background"""
        actions.app.notify("Talon sync started")
        threading.Thread(target=_run, daemon=True).start()
