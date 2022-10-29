# Note: board array should be rows of columns
from pos import BoardPos, Pos
import draw
import config
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
        self.lastHoveredOver = None
        # globals.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
    def validate(self, boardPos, isTaking=False):
        if isTaking:
            for take in self.possibleTakes:
                print(take.boardPos)
                if (take.pieceToTake and take.pieceToTake.boardPos == boardPos) or take.boardPos == boardPos: # ahem
                    return True
            return False
        for move in self.possibleMoves:
            if move.boardPos == boardPos:
                return True
        return False
    # def movePiece(self, newSquare, piece, isTaking=False):
    def movePiece(self, newSquare, piece, isTaking=False):
        # if not self.validate(newSquare.boardPos, isTaking):
        if not self.validate(newSquare.boardPos, isTaking):
            return
        piece.square.setPiece(None)
        piece.snap(newSquare.boardPos)
        if piece.imgName == "pawn": # bad code but I'll only change it if another piece is like this
            piece.notMoved = False
            piece.canEnPassant = True
    def takePiece(self, piece):
        if not self.validate(piece.boardPos, True):
            return False
        piece.deleteImg()
        self.taken[piece.color].append(piece)
        piece.square.setPiece(None)
        return True
    def moveSelected(self, boardPos):
        selected = self.selected
        square = self.getSquare(boardPos)
        self.unselect()
        self.movePiece(square, selected)
    def takenBySelected(self, square):
        selected = self.selected
        pieceToTake = square.pieceToTake
        if self.takePiece(pieceToTake):
            self.unselect()
            self.movePiece(square, selected, True)
    def select(self, piece):
        self.unselect()
        self.selected = piece
        piece.square.color(draw.ORANGE)
        self.possibleMoves, self.possibleTakes = piece.getMoves()
        for square in self.possibleMoves:
            square.highlight(HighlightType.Move)
        for square in self.possibleTakes:
            square.highlight(HighlightType.Take)
    def unselect(self):
        if self.selected:
            self.selected.unselect()
            for square in self.possibleMoves:
                square.unhighlight()
            for square in self.possibleTakes:
                square.unhighlight()
            self.selected = None
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
