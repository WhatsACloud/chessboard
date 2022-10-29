from boardClass import Board
from globals import globals
"""
for sake of simplicity:
    Board starts at top left, which is the side where black is
"""

def initBoard(startPos, Square):
    globals.board = Board(startPos)
