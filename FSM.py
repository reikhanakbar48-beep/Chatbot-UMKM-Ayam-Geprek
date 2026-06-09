from enum import Enum

class State(Enum):
    IDLE = 1
    ORDERING = 2
    CONFIRM_PAYMENT = 3
