from enum import Enum, auto


class CameraActions(Enum):
    MOVE_FORWARD = auto()
    MOVE_BACKWARDS = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    TURN_UP = auto()
    TURN_DOWN = auto()
