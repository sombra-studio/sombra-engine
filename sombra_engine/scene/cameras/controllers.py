from sombra_engine.constants.actions import CameraActions as actions
from sombra_engine.scene.cameras import Camera


class Control:
    """
    The control for a camera handles input conveniently
    """
    def handle_action(self, target: Camera, action: actions):
        pass


class FPSControl(Control):
    def handle_action(self, target: Camera, action: actions):
        if action == actions.MOVE_FORWARD:
            target.position += target.forward * target.speed
        elif action == actions.MOVE_BACKWARDS:
            target.position -= target.backward * target.speed
