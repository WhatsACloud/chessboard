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
    imgName = "rook"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(horizontal)

class Bishop(Piece):
    imgName = "bishop"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(diagonal)

def cond(piece):
    return piece.notMoved

def canEnPassant(toTake, piece):
    return piece.imgName == "pawn" and toTake.imgName == "pawn" and toTake.canEnPassant

class Pawn(Piece):
    imgName = "pawn"
    def __init__(self, boardPos, color):
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
    def canPromote(self, boardPos):
        end = 0
        if self.color == Color.black:
            end = 7
        return boardPos.y == end
    def promote(self, toMoveTo):
        globals.board.newPromotionPrompt(self, toMoveTo) # okay that newSquare variable is just disgraceful

class Queen(Piece):
    imgName = "queen"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(diagonal + horizontal)

class King(Piece):
    imgName = "king"
    def __init__(self, boardPos, color):
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
    imgName = "knight"
    def __init__(self, boardPos, color):
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
