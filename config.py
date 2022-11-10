# board config
SQUARE_LENGTH = 60
BOARD_LENGTH = 8
startX, startY = 100, 100

# window config
WIDTH, HEIGHT = 200, 200

# misc
FONT = "TKDefaultFont"

# probably a bad idea
class Color():
    black = "black"
    white = "white"

def changeColor(color):
    if color == Color.black:
        return Color.white
    return Color.black
