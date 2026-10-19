from talon import Module, ctrl

mod = Module()
mod.tag("navigation")


@mod.action_class
class Actions:
    def hold_right_key():
        """Press and hold the right arrow key"""
        ctrl.key_press("right", down=True)

    def release_right_key():
        """Release the right arrow key"""
        ctrl.key_press("right", up=True)
