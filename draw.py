from pos import Pos, BoardPos
import canvas
from config import SQUARE_LENGTH

BLACK = "#076e00"
WHITE = "#ffffe3"
ORANGE = "#ffbb00"
GREY = "#cfcfcf"

def switchColor(color):
    if color == BLACK:
        return WHITE
    if color == WHITE:
        return BLACK
def drawSquare(pos, color):
    startX, startY = pos.x, pos.y
    return canvas.canvas.create_rectangle(
            startX,
            startY,
            startX + SQUARE_LENGTH,
            startY + SQUARE_LENGTH,
            outline=color,
            fill=color
        )
