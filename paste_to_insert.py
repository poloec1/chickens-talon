from talon import Module, ctrl, actions

mod = Module()
mod.tag("navigation")

@mod.action_class
    class Actions:
    def hold_right_key():
        ctrl.key_press("right", down=True)

    def release_right_key():
        ctrl.key_press("right", up=True)