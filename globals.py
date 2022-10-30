from enum import Enum
from config import Color

class HighlightType(Enum):
    Move = 1
    Take = 2
    Hover = 3

class globals():
    board = None
    canvas = None
    turn = None
    attackAngles = {
        Color.white: {}, # where white will be attacked
        Color.black: {} # where black will be attacked
    } # for checking if king is checked
