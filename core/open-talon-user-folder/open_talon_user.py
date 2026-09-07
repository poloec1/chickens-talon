import os
import subprocess
from talon import Module, actions

mod = Module()

@mod.action_class
class Actions:
    def open_folder(path: str):
        """Open a folder in Finder (macOS)"""
        print(f"[DEBUG] open_folder called with path: {path}")
        if os.path.isdir(path):
            print(f"[DEBUG] Folder exists: {path}")
            subprocess.run(["open", path])
        else:
            print(f"[DEBUG] Folder does not exist: {path}")
            actions.app.notify(f"Folder does not exist: {path}")