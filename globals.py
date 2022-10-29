from enum import Enum

class HighlightType(Enum):
    Move = 1
    Take = 2
    Hover = 3

class globals():
    board = None
    canvas = None
    turn = None
