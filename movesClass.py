from pos import BoardPos
from board import getBoard
import config
import copy

class Direction():
    up = BoardPos(0, -1)
    down = BoardPos(0, 1)
    left = BoardPos(-1, 0)
    right = BoardPos(1, 0)

class Move():
    def __init__(self, directions, cond=None, amt=config.BOARD_LENGTH):
        self.directions = directions
        self.cond = cond
        self.amt = amt
    def can(self, piece):
        if self.cond:
            return self.cond(piece)
        return True
    def calc(self, piece):
        if not self.can(piece): return []
        moves = []
        takes = []
        currentPos = copy.deepcopy(piece.boardPos)
        for i in range(self.amt):
            for direction in self.directions:
                currentPos += direction
            if currentPos.exceedsBoard():
                break
            square = getBoard().getSquare(currentPos)
            if square.piece:
                if square.piece.color != piece.color:
                    takes.append(square)
                break
            moves.append(square)
        return moves, takes
    
def changeAmts(moves, amt):
    arr = []
    for move in moves:
        arr.append(Move(move.directions, amt=1))
    return arr