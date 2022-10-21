from pos import BoardPos
from board import getBoard
import config
import copy

class Direction():
    up = BoardPos(-1, 0)
    down = BoardPos(1, 0)
    left = BoardPos(0, -1)
    right = BoardPos(0, 1)

class Move():
    def __init__(self, directions, cond=None, amt=config.BOARD_LENGTH):
        self.directions = directions
        self.cond = cond
        self.amt = amt
    def can(self, boardPos):
        if self.cond:
            return self.cond(boardPos)
        return True
    def calc(self, boardPos):
        if not self.can(boardPos): return []
        moves = []
        currentPos = copy.deepcopy(boardPos)
        for i in range(self.amt):
            for direction in self.directions:
                currentPos += direction
            if currentPos.exceedsBoard():
                break
            square = getBoard().getSquare(currentPos)
            if square.piece:
                break
            moves.append(square)
        return moves
