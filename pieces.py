from movesClass import Direction, Move, changeAmts
from piece import Piece
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

class Pawn(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "pawn"
        super().__init__(boardPos, color)
        self.moved = False
        self.notMoved = True
        direction = None
        if color == Color.black:
            direction = Direction.down
        else:
            direction = Direction.up
        def cond(piece):
            if piece.notMoved:
                return True
            return False
        self.setMoves([
            Move([direction], amt=1),
            Move([direction * 2], amt=1, cond=cond)
        ])

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