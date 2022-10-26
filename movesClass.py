from pos import BoardPos
from board import getBoard
import config
import copy

class Direction():
    up = BoardPos(0, -1)
    down = BoardPos(0, 1)
    left = BoardPos(-1, 0)
    right = BoardPos(1, 0)

class CalcIterator:
    def __init__(self, directions, currentPos, amt):
        self.directions = directions
        self.currentPos = currentPos
        self.end = amt
        self.count = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.count >= self.end:
            raise StopIteration
        self.count += 1
        for direction in self.directions:
            self.currentPos += direction
        if self.currentPos.exceedsBoard():
            raise StopIteration
        square = getBoard().getSquare(self.currentPos)
        return square

class Move():
    def __init__(self, directions, cond=None, amt=config.BOARD_LENGTH):
        self.directions = directions
        self.cond = cond
        self.amt = amt
    def can(self, piece, square):
        if self.cond:
            return self.cond(piece, getBoard(), square)
        if square.piece:
            return True
        return False
    def calc(self, piece, isTake=False):
        moves = []
        currentPos = copy.deepcopy(piece.boardPos)
        if isTake:
            for square in CalcIterator(self.directions, currentPos, self.amt):
                if self.can(piece, square):
                    break
        else:
            for square in CalcIterator(self.directions, currentPos, self.amt):
                if square.piece or not self.can(piece, square):
                    break
                moves.append(square)
        return moves
    
def changeAmts(moves, amt):
    arr = []
    for move in moves:
        arr.append(Move(move.directions, amt=1))
    return arr