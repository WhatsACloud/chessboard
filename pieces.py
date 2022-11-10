from movesClass import Direction, Move, Take, changeAmts
from piece import Piece
from pos import BoardPos
import config
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
        self.notMoved = True

class Bishop(Piece):
    imgName = "bishop"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(diagonal)

def cond(piece, toMoveTo):
    return piece.imgName == "pawn" and piece.state == globals.PawnStates.OriginalPos

def canEnPassant(toTake, piece):
    return piece.imgName == "pawn" and toTake.imgName == "pawn" and toTake.state == globals.PawnStates.CanEnPassant

class Pawn(Piece):
    imgName = "pawn"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.state = globals.PawnStates.OriginalPos
        direction = Direction.up
        if color == config.Color.black:
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
        globals.board.pawns.append(self)
    def canPromote(self, boardPos):
        end = 0
        if self.color == config.Color.black:
            end = 7
        return boardPos.y == end
    def promote(self, toMoveTo):
        globals.board.newPromotionPrompt(self, toMoveTo) # okay that newSquare variable is just disgraceful

class Queen(Piece):
    imgName = "queen"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(diagonal + horizontal)

def canCastleRight(piece, toMoveTo):
    if isinstance(piece, King) and piece.wouldSelfBeChecked(piece, toMoveTo):
        return False
    if isinstance(piece, King) and piece.isChecked():
        return False
    rightRook = globals.board.getSquare(BoardPos(config.BOARD_LENGTH-1, piece.boardPos.y)).piece # closer rook
    if type(rightRook) == Rook and piece.notMoved and rightRook.notMoved:
        for i in range(piece.boardPos.x+1, config.BOARD_LENGTH-1):
            pieceInPath = globals.board.getSquare(BoardPos(i, piece.boardPos.y)).piece
            if pieceInPath:
                return False
        return True
    return False

def canCastleLeft(piece, toMoveTo):
    if isinstance(piece, King) and piece.wouldSelfBeChecked(piece, toMoveTo):
        return False
    if isinstance(piece, King) and piece.isChecked():
        return False
    leftRook = globals.board.getSquare(BoardPos(0, piece.boardPos.y)).piece # farther rook
    if type(leftRook) == Rook and piece.notMoved and leftRook.notMoved:
        for i in range(1, piece.boardPos.x):
            pieceInPath = globals.board.getSquare(BoardPos(i, piece.boardPos.y)).piece
            if pieceInPath:
                return False
        return True
    return False

def afterCastleRight(piece):
    rook = globals.board.getSquare(BoardPos(7, piece.boardPos.y)).piece
    rook.snap(BoardPos(5, piece.boardPos.y))

def afterCastleLeft(piece):
    rook = globals.board.getSquare(BoardPos(0, piece.boardPos.y)).piece
    rook.snap(BoardPos(3, piece.boardPos.y))

class Attacker: # container class
    def __init__(self, attacker, route):
        self.attacker = attacker
        self.route = route # as in the path of attack

class King(Piece):
    imgName = "king"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(
            [
                *changeAmts(diagonal, 1),
                *changeAmts(horizontal, 1),
                Move([Direction.right * 2], cond=canCastleRight, after=afterCastleRight, amt=1),
                Move([Direction.left * 2], cond=canCastleLeft, after=afterCastleLeft, amt=1),
            ],
            [
                *changeAmts(diagonal, 1, Take),
                *changeAmts(horizontal, 1, Take),
            ]
        )
        self.notMoved = True
        globals.board.kings[color] = self
    def isChecked(self):
        return self.canBeTaken(self)
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
    def canBeTaken(self, piece):
        for pieceType in globals.attackAngles[piece.color]:
            takes = globals.attackAngles[piece.color][pieceType]
            for take in takes:
                # allTakes = []
                # # print(take)
                # for square in take.calc(self, False):
                    # if type(globals.board.getSquare(square.boardPos).piece) == pieceType:
                        # allTakes.append(square)
                # if len(allTakes) > 0:
                    # return True
                square = take.calc(piece, False)
                if square and square.piece and type(square.piece) == pieceType:
                    return True
        return False
    def getAttackers(self):
        attackers = []
        for pieceType in globals.attackAngles[self.color]:
            takes = globals.attackAngles[self.color][pieceType]
            for take in takes:
                squares = take.getPath(self, False)
                if len(squares) > 0:
                    attackers.append(Attacker(squares.pop().piece, squares))
        return attackers
    def isCheckmated(self):
        attackers = self.getAttackers()
        if len(attackers) == 0: # no attackers
            return False
        if len(attackers) < 2: # if only one attacker
            if self.canBeTaken(attackers[0].attacker): # and that attacker can be taken
                return False
            for attacker in attackers:
                for square in attacker.route: # can a piece block it
                    if square.piece: # checks if there is piece of opposite color
                        if square.piece.color != self.color:
                            attackTypes = globals.attackAngles[config.changeColor(self.color)]
                            for pieceType in attackTypes:
                                takes = attackTypes[pieceType]
                                for take in takes:
                                    takeSquare = take.calc(square.piece, False) # as in possible take from current square
                                    if type(takeSquare.piece) == pieceType and self.wouldSelfBeChecked(takeSquare.piece, square):
                                        return False
                    else:
                        moveTypes = globals.moveAngles[config.changeColor(self.color)]
                        for pieceType in moveTypes:
                                moves = moveTypes[pieceType]
                                for take in moves:
                                    samplePiece = Pawn(square.boardPos, self.color)
                                    moveSquare = take.calc(samplePiece, False) # as in possible move from current square
                                    if moveSquare and moveSquare.boardPos == BoardPos(4, 5):
                                        print(
                                            moveSquare,
                                            moveSquare.piece.color == self.color,
                                            type(moveSquare.piece) == pieceType,
                                            self.wouldSelfBeChecked(moveSquare.piece, square),
                                        )
                                    samplePiece.delete()
                                    if ( # its a take because we are checking if a piece exists in moves
                                        moveSquare
                                        and moveSquare.piece.color == config.changeColor(self.color)
                                        and type(moveSquare.piece) == pieceType
                                        and self.wouldSelfBeChecked(moveSquare.piece, square)
                                    ):
                                        return False
        moves, takes = self.getMoves()
        if len([*moves, *takes]) > 0: # has square to move to
            return False
        return True
        
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
