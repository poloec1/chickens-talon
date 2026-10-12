from talon import Module

mod = Module()

# Kiro is a VS Code fork; register its bundle under the community "vscode" app so
# it inherits all VS Code contexts (command server, Cursorless, language mode).
mod.apps.vscode = """
os: mac
and app.bundle: dev.kiro.desktop
"""
