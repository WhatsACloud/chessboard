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

class AttrHist: # my iq is equal to the number of girls who aren't creeped out by me i.e. -10
    def __init__(self, val):
        self.hist = {}
        self.indexes = []
        self.set(val)
    def set(self, item):
        # print(self.hist, self.indexes)
        # print(globals.board.currentIndex)
        if globals.board.currentIndex != globals.board.highestIndex:
            print("helpkdfjsdffbqefuqrefqrefuqefuqrefbwqefjqefuqefueqrf")
            toRemove = self.indexes[globals.board.currentIndex:]
            self.indexes = self.indexes[:globals.board.currentIndex]
            for index in toRemove:
                del self.hist[index]
        self.hist[globals.board.currentIndex] = item
        self.indexes.append(globals.board.currentIndex)
    def getCurrent(self):
        if globals.board.currentIndex in self.hist:
            return self.hist[globals.board.currentIndex]
        return self.hist[self.indexes[-1]]

class Rook(Piece):
    imgName = "rook"
    def __init__(self, boardPos, color):
        super().__init__(boardPos, color)
        self.setMoves(horizontal)
        self._notMoved = AttrHist(True)
    @property
    def notMoved(self):
        # print(self.boardPos, self._notMoved.hist, self._notMoved.indexes)
        print(self._notMoved.hist, self._notMoved.indexes, globals.board.currentIndex, globals.board.highestIndex)
        return self._notMoved.getCurrent()
    @notMoved.setter
    def notMoved(self, val):
        self._notMoved.set(val)

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
        self._state = AttrHist(globals.PawnStates.OriginalPos)
    @property
    def state(self):
        return self._state.getCurrent()
    @state.setter
    def state(self, state):
        self._state.set(state)
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
    print("why")
    if isinstance(piece, King) and piece.wouldSelfBeChecked(piece, toMoveTo):
        return False
    print("why 1")
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

class After:
    def __init__(self, after, reverse):
        self.after = after
        self.reverse = reverse

def reverseAfterCastleRight(piece):
    rook = globals.board.getSquare(BoardPos(5, piece.boardPos.y)).piece
    if type(rook) != Rook:
        return
    rook.snap(BoardPos(7, piece.boardPos.y))

def reverseAfterCastleLeft(piece):
    rook = globals.board.getSquare(BoardPos(3, piece.boardPos.y)).piece
    print("why", rook)
    if type(rook) != Rook:
        return
    rook.snap(BoardPos(0, piece.boardPos.y))

def afterCastleRight(piece):
    rook = globals.board.getSquare(BoardPos(7, piece.boardPos.y)).piece
    if type(rook) != Rook:
        return
    rook.snap(BoardPos(5, piece.boardPos.y))

def afterCastleLeft(piece):
    rook = globals.board.getSquare(BoardPos(0, piece.boardPos.y)).piece
    if type(rook) != Rook:
        return
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
                Move([Direction.right * 2], cond=canCastleRight, after=After(afterCastleRight, reverseAfterCastleRight), amt=1),
                Move([Direction.left * 2], cond=canCastleLeft, after=After(afterCastleLeft, reverseAfterCastleLeft), amt=1),
            ],
            [
                *changeAmts(diagonal, 1, Take),
                *changeAmts(horizontal, 1, Take),
            ]
        )
        globals.board.kings[color] = self
        self._notMoved = AttrHist(True)
    @property
    def notMoved(self):
        return self._notMoved.getCurrent()
    @notMoved.setter
    def notMoved(self, val):
        self._notMoved.set(val)
    def isChecked(self):
        for pieceType in globals.attackAngles[self.color]:
            takes = globals.attackAngles[self.color][pieceType]
            for take in takes:
                # allTakes = []
                # # print(take)
                # for square in take.calc(self, False):
                    # if type(globals.board.getSquare(square.boardPos).piece) == pieceType:
                        # allTakes.append(square)
                # if len(allTakes) > 0:
                    # return True
                square = take.calc(self, False)
                if square and square.piece and type(square.piece) == pieceType:
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
    def anyMoveAvailable(self):
        for piece in globals.board.pieces[self.color]:
            moves, takes = piece.getMoves()
            if len([*moves, *takes]) > 0:
                return False
        return True
    def isStalemated(self):
        if self.isChecked():
            return False
        return self.anyMoveAvailable()
    def isCheckmated(self):
        if not self.isChecked():
            return False
        return self.anyMoveAvailable()
        
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
