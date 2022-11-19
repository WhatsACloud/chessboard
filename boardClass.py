# Note: board array should be rows of columns
from pos import BoardPos, Pos
import draw
import config
import pieces
from promotePrompt import PromotionPrompt
from notification import Notification
from square import Square
from globals import globals, HighlightType
from extraUI import extraUI
import math

class Taken:
    def __init__(self):
        self.table = {
            config.Color.black: [],
            config.Color.white: [],
        }
    def add(self, piece):
        self.table[piece.color].append(piece)
        globals.board.extraUI.takenPieces[piece.color].update()
    def getTable(self, color):
        return self.table[color]


class Board(): # rows and columns start at 0, not 1
    def __init__(self, startPos):
        self.reversed = False
        self.extraUI = extraUI(startPos)
        self.startPos = startPos
        self.board = self.createBoard()
        self.possibleMoves = []
        self.taken = Taken()
        self.take = {
            config.Color.black: [],
            config.Color.white: [],
        }
        self.selected = None
        self.canUnselect = False # used only in self.clickedOut
        self.promotionPrompt = None
        self.pieces = {
            config.Color.white: [],
            config.Color.black: [],
        }
        self.kings = {
            config.Color.white: None,
            config.Color.black: None,
        }
        self.pawns = []
        self.haveEnPassant = []
        self.lastHoveredOver = None
        globals.canvas.bindToResize(self.center)
        self.bindEvents()
        # globals.canvas.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
    def delete(self):
        for row in self.board:
            for square in row:
                square.delete()
                del square
        globals.canvas.unbindAllResize()
        self.unbindEvents()
    def bindEvents(self):
        globals.canvas.canvas.bind("<Button-1>", self.clickedOut)
    def unbindEvents(self):
        globals.canvas.canvas.unbind_all("<Button-1>")
    def clickedOut(self, e):
        if self.selected and self.canUnselect:
            return self.unselectFully()
        self.canUnselect = True
    def validate(self, boardPos, isTaking=False):
        if isTaking:
            for take in self.possibleTakes:
                if (take.pieceToTake and take.pieceToTake.boardPos == boardPos) or take.boardPos == boardPos: # ahem
                    return True
            return False
        for move in self.possibleMoves:
            if move.boardPos == boardPos:
                return True
        return False
    # def movePiece(self, newSquare, piece, isTaking=False):
    def nextTurn(self):
        for pawn in self.pawns:
            if pawn in self.haveEnPassant:
                pawn.state = globals.PawnStates.Matured
                del self.haveEnPassant[self.haveEnPassant.index(pawn)]
                continue
            if pawn.state == globals.PawnStates.CanEnPassant:
                self.haveEnPassant.append(pawn)
        globals.turn = config.changeColor(globals.turn)
        currentKing = self.kings[globals.turn]
        if currentKing.isCheckmated():
            Notification(f"{config.changeColor(globals.turn)} wins!")
        elif currentKing.isStalemated():
            Notification("Stalemate!")
        self.reverseBoard()
    def newPromotionPrompt(self, piece, newSquare): # ah yes i am very intelligent
        if self.promotionPrompt:
            self.promotionPrompt.delete()
        self.promotionPrompt = PromotionPrompt(piece, newSquare)
    def reverseBoard(self): # visually
        self.reversed = globals.turn == config.Color.black
        for row in self.board:
            for square in row:
                square.moveto(self.getPosFromBoardPos(square.boardPos))
        self.extraUI.takenPieces[config.Color.white].updateYAxis()
        self.extraUI.takenPieces[config.Color.black].updateYAxis()
        self.extraUI.takenPieces[config.Color.white].update()
        self.extraUI.takenPieces[config.Color.black].update()
    def checkCanMovePiece(self, newSquare, piece, isTaking=False): # as in can move to SQUARE
        if not self.isCorrectColor(piece):
            return False
        if not self.validate(newSquare.boardPos, isTaking):
            return False
        origSquare = piece.square
        if self.kings[piece.color].wouldSelfBeChecked(piece, newSquare):
            return False
        if piece.imgName == "pawn": # bad code but I'll only change it if another piece is like this
            if piece.state == globals.PawnStates.OriginalPos:
                piece.state = globals.PawnStates.CanEnPassant
            if piece.canPromote(newSquare.boardPos):
                piece.promote(newSquare.boardPos)
                return False
        if piece.imgName == "rook" or piece.imgName == "king":
            piece.notMoved = False
        return True
    def movePiece(self, boardPos, piece): # should ONLY move piece and call nextTurn
        piece.snap(boardPos)
        # piece.movetoPos(self.getPosFromBoardPos(boardPos))
        self.nextTurn()
    def takePiece(self, piece):
        if not (piece and self.validate(piece.boardPos, True)):
            return False
        piece.remove()
        piece.square.setPiece(None)
        return True
    def moveSelected(self, square):
        selected = self.selected
        selected.unselect()
        if self.checkCanMovePiece(square, selected):
            self.movePiece(square.boardPos, selected)

        square.runAfterFunc(selected)
        selected.reset()
    def takenBySelected(self, square):
        selected = self.selected
        pieceToTake = square.pieceToTake # why is this None?
        if self.takePiece(pieceToTake):
            self.unselectFully()
            if self.checkCanMovePiece(square, selected, True):
                self.movePiece(square.boardPos, selected)
        selected.reset()
    def isCorrectColor(self, piece):
        return globals.turn == piece.color
    def select(self, piece):
        if not self.isCorrectColor(piece):
            return
        self.unselectFully()
        self.selected = piece
        piece.square.color(draw.ORANGE)
        self.possibleMoves, self.possibleTakes = piece.getMoves()
        for square in self.possibleMoves:
            square.highlight(HighlightType.Move)
        for square in self.possibleTakes:
            square.highlight(HighlightType.Take)
    def unhighlight(self):
        for square in self.possibleMoves:
            square.unhighlight()
        for square in self.possibleTakes:
            square.unhighlight()
    def unselect(self): # i cant be bothered at this point
        if self.selected:
            self.selected.unselect()
            self.selected = None
            return True
        return False
    def unselectFully(self):
        self.canUnselect = False
        if self.unselect():
            self.unhighlight()
    def getPosFromBoardPos(self, boardPos):
        reversedBoardPos = (config.BOARD_LENGTH - 1) - boardPos
        pos = self.startPos + boardPos * config.SQUARE_LENGTH
        if self.reversed:
            pos = self.startPos + reversedBoardPos * config.SQUARE_LENGTH
        return pos
    def getSquare(self, pos):
        return self.board[pos.x][pos.y]
    def getSquareWhichPosInside(self, pos):
        start = self.getPosFromBoardPos(BoardPos(0, 0))
        end = self.getPosFromBoardPos(BoardPos(config.BOARD_LENGTH, config.BOARD_LENGTH))
        if pos.inside(start, end):
            boardPos = math.floor((pos - self.startPos) / Pos(config.SQUARE_LENGTH, config.SQUARE_LENGTH))
            return self.board[int(boardPos.x)][int(boardPos.y)]
        return None
    def createBoard(self):
        color = draw.BLACK
        length = config.BOARD_LENGTH
        boardArr = []
        for row in range(length):
            color = draw.switchColor(color)
            boardArr.append([])
            for col in range(length):
                boardPos = BoardPos(row, col)
                square = Square(self.getPosFromBoardPos(boardPos), boardPos, color)
                color = draw.switchColor(color)
                boardArr[row].append(square)
        return boardArr
    def center(self): # centers board
        middle = globals.canvas.getDimensions() / 2
        diff = config.BOARD_LENGTH / 2 * config.SQUARE_LENGTH
        start = middle - Pos(diff, diff)
        self.startPos = start
        for row in self.board:
            for square in row:
                square.moveto(self.getPosFromBoardPos(square.boardPos))
