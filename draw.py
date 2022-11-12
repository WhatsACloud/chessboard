from pos import Pos, BoardPos
from globals import globals
import canvasObjs

BLACK = "#076e00"
WHITE = "#ffffe3"
ORANGE = "#ffbb00"
GREY = "#cfcfcf"
LIGHTGREY = "#f0f0f0"
RED = "#fc0317"
DARKRED = "#6e0009"

def switchColor(color):
    if color == BLACK:
        return WHITE
    if color == WHITE:
        return BLACK
