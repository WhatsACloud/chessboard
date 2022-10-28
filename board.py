from boardClass import Board
"""
for sake of simplicity:
    Board starts at top left, which is the side where black is
"""

board = None
def getBoard():
    return board

def initBoard(startPos, Square):
    global board
    board = Board(startPos)
    return board
