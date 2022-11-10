# Note: board array should be rows of columns
from pos import BoardPos, Pos
import draw
import config
import pieces
from promotePrompt import PromotionPrompt
from square import Square
from globals import globals, HighlightType

class Board(): # rows and columns start at 0, not 1
    def __init__(self, startPos):
        self.startPos = startPos
        self.board = self.createBoard()
        self.possibleMoves = []
        self.taken = {
            config.Color.black: [],
            config.Color.white: [],
        }
        self.selected = None
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
        # globals.canvas.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
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
        checkmated = self.kings[globals.turn].isCheckmated()
        print(checkmated)
    def newPromotionPrompt(self, piece, newSquare): # ah yes i am very intelligent
        if self.promotionPrompt:
            self.promotionPrompt.delete()
        self.promotionPrompt = PromotionPrompt(piece, newSquare)
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
        self.nextTurn()
    def takePiece(self, piece):
        if not self.validate(piece.boardPos, True):
            return False
        piece.remove()
        piece.square.setPiece(None)
        return True
    def moveSelected(self, square):
        selected = self.selected
        self.unselect()
        if self.checkCanMovePiece(square, selected):
            self.movePiece(square.boardPos, selected)

        square.runAfterFunc(selected)
        self.unhighlight()
    def takenBySelected(self, square):
        selected = self.selected
        pieceToTake = square.pieceToTake
        if self.takePiece(pieceToTake):
            self.unselectFully()
            if self.checkCanMovePiece(square, selected, True):
                self.movePiece(square.boardPos, selected)
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
        if self.unselect():
            self.unhighlight()
    def getPosFromBoardPos(self, boardPos):
        return Pos(self.startPos.x + boardPos.x * config.SQUARE_LENGTH, self.startPos.y + boardPos.y * config.SQUARE_LENGTH)
    def getSquare(self, pos):
        return self.board[pos.x][pos.y]
    def click(self, e):
        mousePos = Pos(e.x, e.y)
        square = self.getSquareWhichPosInside(mousePos)
        if square:
            square.select()
    def getSquareWhichPosInside(self, pos):
        start = self.getPosFromBoardPos(BoardPos(0, 0))
        end = self.getPosFromBoardPos(BoardPos(config.BOARD_LENGTH, config.BOARD_LENGTH))
        if pos.inside(start, end):
            boardPos = round(pos / Pos(config.SQUARE_LENGTH, config.SQUARE_LENGTH)) - BoardPos(2, 2)
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
