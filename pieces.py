from movesClass import Direction, Move, Take, changeAmts
from piece import Piece
from pos import BoardPos
from config import Color
from globals import globals

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

def cond(piece):
    return piece.notMoved

def canEnPassant(toTake, piece):
    return piece.imgName == "pawn" and toTake.imgName == "pawn" and toTake.canEnPassant

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
        globals.board.kings[color] = self
    def isChecked(self):
        for pieceType in globals.attackAngles[self.color]:
            takes = globals.attackAngles[self.color][pieceType]
            for take in takes:
                allTakes = []
                for square in take.calc(self, False):
                    if type(globals.board.getSquare(square.boardPos).piece) == pieceType:
                        allTakes.append(square)
                if len(allTakes) > 0:
                    return True
        return False
    def wouldSelfBeChecked(self, origPiece, newSquare):
        returnVal = False
        origSquare = origPiece.square
        newSquarePiece = newSquare.piece
        origPiece.moveto(newSquare.boardPos)
        if self.isChecked():
            returnVal = True
        origPiece.moveto(origSquare.boardPos)
        newSquare.piece = newSquarePiece
        return returnVal
        
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
