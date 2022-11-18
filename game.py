# hell yeah lets make everything a class
from square import Square
from board import initBoard
from pos import Pos, BoardPos
from globals import globals, HighlightType
import config
import pieces
import draw
import gc

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
        self.startPos = startPos
        self.length = length
        self.init()
    def init(self):
        initBoard(self.startPos, Square)
        globals.turn = config.Color.white
        self.setUp()
    def setUp(self):
        setupPieces(config.Color.black)
        setupPieces(config.Color.white)

        # pieces.King(BoardPos(4, 7), config.Color.black)
        # pieces.Rook(BoardPos(0, 7), config.Color.black)
        # pieces.Rook(BoardPos(7, 7), config.Color.black)
        # pieces.King(BoardPos(4, 0), config.Color.white)
        # pieces.Rook(BoardPos(0, 0), config.Color.white)
        # pieces.Pawn(BoardPos(4, 1), config.Color.black)
    def reset():
        print(len(gc.get_objects()))
        del globals.board
        print(len(gc.get_objects()))
        self.init()
