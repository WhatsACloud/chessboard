from pos import BoardPos
from globals import globals
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
        square = globals.board.getSquare(self.currentPos)
        return square

# class PossibleMove:
    # def __init__(self, square, afterFunc):
        # self.square = square
        # self.afterFunc = afterFunc

class Move:
    def __init__(self, directions, cond=None, amt=config.BOARD_LENGTH, after=None):
        self.directions = directions
        self.cond = cond
        self.after = after
        self.amt = amt
        self.after = after
    def __repr__(self):
        string = "["
        for direction in self.directions:
            string += (str(direction) + ", ")
        return string[0:-2] + f", {self.amt}]"
    def can(self, origPiece, square):
        if square.piece:
            return False
        if globals.board.kings[origPiece.color].wouldSelfBeChecked(origPiece, square):
            return False
        if self.cond:
            return self.cond(origPiece, square)
        return True
    def calc(self, piece):
        moves = set()
        currentPos = copy.deepcopy(piece.boardPos)
        for square in CalcIterator(self.directions, currentPos, self.amt):
            if square.piece or not self.can(piece, square):
                break
            if self.after:
                square.after = self.after
            moves.add(square)
        return moves

class Take(Move):
    def __init__(self, directions, cond=None, amt=config.BOARD_LENGTH, pieceOffset=BoardPos(0, 0)):
        super().__init__(directions, cond, amt)
        self.pieceOffset = pieceOffset
    def canTake(self, piece, origPiece):
        if piece.color == origPiece.color:
            return False
        if self.cond:
            return self.cond(piece, origPiece)
        return True
    def getPieceToTake(self, square):
        pieceSquare = globals.board.getSquare(square.boardPos + self.pieceOffset)
        if pieceSquare:
            return pieceSquare.piece
        return None
    def getPath(self, piece, checkIsCheck=True):
        squares = []
        currentPos = copy.deepcopy(piece.boardPos)
        for square in CalcIterator(self.directions, currentPos, self.amt):
            pieceToTake = self.getPieceToTake(square)
            # if piece.imgName == "pawn" and self.amt == 8:
                # if square.boardPos == BoardPos(4, 5):
                    # print("lasdfjsdjf", square.piece, pieceToTake, square.boardPos)
            if checkIsCheck and pieceToTake and globals.board.kings[piece.color].wouldSelfBeChecked(piece, pieceToTake.square):
                break
            squares.append(square)
            # if piece.imgName == "pawn" and self.amt == 8:
                # if square.boardPos == BoardPos(4, 5):
                    # print("2", square.piece, pieceToTake, square.boardPos)
            if pieceToTake and self.canTake(pieceToTake, piece):
                square.pieceToTake = pieceToTake
                return squares
            if square.piece:
                break
        return []
    def calc(self, piece, checkIsCheck=True):
        currentPos = copy.deepcopy(piece.boardPos)
        squares = self.getPath(piece, checkIsCheck)
        if len(squares) > 0:
            return squares[-1]
        # for square in CalcIterator(self.directions, currentPos, self.amt):
            # pieceToTake = self.getPieceToTake(square)
            # if checkIsCheck and pieceToTake and globals.board.kings[piece.color].wouldSelfBeChecked(piece, pieceToTake.square):
                # break
            # if pieceToTake and self.canTake(pieceToTake, piece):
                # square.pieceToTake = pieceToTake
                # return square
            # if square.piece:
                # break
        return None
    
def changeAmts(moves, amt, theClass=Move): # wow
    arr = []
    for move in moves:
        arr.append(theClass(move.directions, amt=1))
    return arr
