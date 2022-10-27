from movesClass import Direction, Move, Take, changeAmts
from piece import Piece
from pos import BoardPos
from config import Color

diagonal = [
    Move([Direction.up, Direction.left]),
    Move([Direction.left, Direction.down]),
    Move([Direction.down, Direction.right]),
    Move([Direction.right, Direction.up]),
]

horizontal = [
    Move([Direction.up]),
    Move([Direction.down]),
    Move([Direction.left]),
    Move([Direction.right]),
]

class Rook(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "rook"
        super().__init__(boardPos, color)
        self.setMoves(horizontal)

class Bishop(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "bishop"
        super().__init__(boardPos, color)
        self.setMoves(diagonal)

def cond(toTake, board, square):
    return toTake.notMoved

def canEnPassant(toTake, board, square):
    return toTake.imgName == "pawn"

class Pawn(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "pawn"
        super().__init__(boardPos, color)
        self.moved = False
        self.notMoved = True
        self.canEnPassant = True
        direction = Direction.up
        if color == Color.black:
            direction = Direction.down
        self.setMoves(
            [
                Move([direction], amt=1),
                Move([direction], amt=2, cond=cond)
            ],
            [
                Take([direction, Direction.left], amt=1),
                Take([direction, Direction.right], amt=1),
                Take([direction, Direction.left], amt=1, pieceOffset=direction * -1, cond=canEnPassant),
                Take([direction, Direction.right], amt=1, pieceOffset=direction * -1, cond=canEnPassant),
            ]
        )

class Queen(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "queen"
        super().__init__(boardPos, color)
        self.setMoves(diagonal + horizontal)

class King(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "king"
        super().__init__(boardPos, color)
        self.setMoves(
            changeAmts(diagonal, 1)
          + changeAmts(horizontal, 1)
        )
        
class Knight(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "knight"
        super().__init__(boardPos, color)
        self.setMoves([
            Move([Direction.up * 2, Direction.left], amt=1),
            Move([Direction.up * 2, Direction.right], amt=1),
            Move([Direction.down * 2, Direction.left], amt=1),
            Move([Direction.down * 2, Direction.right], amt=1),
            Move([Direction.left * 2, Direction.up], amt=1),
            Move([Direction.left * 2, Direction.down], amt=1),
            Move([Direction.right * 2, Direction.up], amt=1),
            Move([Direction.right * 2, Direction.down], amt=1),
        ])
