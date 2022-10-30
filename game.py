# hell yeah lets make everything a class
from square import Square
from board import initBoard
from pos import Pos, BoardPos
from globals import globals, HighlightType
import config
import pieces
import draw

def setupPieces(color):
    firstRow, secondRow = None, None
    end = config.BOARD_LENGTH-1
    if color == config.Color.black:
        firstRow, secondRow = 0, 1
    else:
        firstRow, secondRow = end, end-1
    pieces.Rook(BoardPos(0, firstRow), color)
    pieces.Rook(BoardPos(end, firstRow), color)
    pieces.Knight(BoardPos(1, firstRow), color)
    pieces.Knight(BoardPos(end-1, firstRow), color)
    pieces.Bishop(BoardPos(2, firstRow), color)
    pieces.Bishop(BoardPos(end-2, firstRow), color)
    pieces.Queen(BoardPos(3, firstRow), color)
    pieces.King(BoardPos(end-3, firstRow), color)
    for i in range(config.BOARD_LENGTH):
        pieces.Pawn(BoardPos(i, secondRow), color)


class Game():
    def __init__(self, startPos, length):
        initBoard(startPos, Square)
        globals.turn = config.Color.white

        # setupPieces(config.Color.black)
        # setupPieces(config.Color.white)

        pieces.King(BoardPos(1, 1), config.Color.black)
        pieces.Queen(BoardPos(4, 4), config.Color.white)
        pieces.Pawn(BoardPos(5, 3), config.Color.black)
        pieces.King(BoardPos(5, 5), config.Color.white)
        pieces.Bishop(BoardPos(3, 3), config.Color.black)

        # pieces.Rook(BoardPos(4, 4), config.Color.black)
        # pieces.Knight(BoardPos(4, 3), config.Color.white)
