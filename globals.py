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
    window = None
    attackAngles = {
        Color.white: {}, # where white will be attacked
        Color.black: {} # where black will be attacked
    } # for checking if king is checked
    class PawnStates:
        OriginalPos = 0
        CanEnPassant = 1
        Matured = 2 # as in it is past the two move thingy
