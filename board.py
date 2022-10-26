# Note: board array should be rows of columns
from enum import Enum
import draw
from pos import BoardPos, Pos
import config
import canvas

"""
for sake of simplicity:
    Board starts at top left, which is the side where black is
"""

class HighlightType(Enum):
    Move = 1
    Take = 2
    Hover = 3

board = None
def getBoard():
    return board

class Square():
    def __init__(self, pos, boardPos, color):
        self.id = draw.drawSquare(pos, color)
        self.boardPos = boardPos
        self.origColor = color
        self.canvasObj = None
        self.highlighted = False
        self.squareHighlight = None
        self.piece = None
        self.bindEvents()
    def bindEvent(self, evt, func):
        canvas.canvas.tag_bind(self.id, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
    def enter(self):
        if board.selected and board.selected.dragging and not self.squareHighlight:
            self.drawSquare()
    def leave(self):
        self.deleteSquare()
    def setPiece(self, piece):
        self.piece = piece
    def click(self, e):
        if not self.highlighted:
            board.unselect()
            return
        board.moveSelected(self.boardPos)
    def drawCircle(self, highlightType):
        startPos = board.getPosFromBoardPos(self.boardPos)
        circleLength = config.SQUARE_LENGTH / 4
        fill = draw.GREY
        width = 1
        if highlightType == HighlightType.Hover:
            return
        if highlightType == HighlightType.Take:
            circleLength *= 3.5
            fill = ''
            width = 5
        offset = config.SQUARE_LENGTH / 2 - circleLength / 2
        self.canvasObj = canvas.canvas.create_oval(
            startPos.x + offset,
            startPos.y + offset,
            startPos.x + offset + circleLength,
            startPos.y + offset + circleLength,
            fill=fill,
            outline=draw.GREY,
            width=width
        )
    def deleteCircle(self):
        if self.canvasObj:
            # canvas.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            canvas.canvas.delete(self.canvasObj)
            self.canvasObj = None
    def drawSquare(self):
        startPos = board.getPosFromBoardPos(self.boardPos)
        self.squareHighlight = canvas.canvas.create_rectangle(
            startPos.x,
            startPos.y,
            startPos.x + config.SQUARE_LENGTH,
            startPos.y + config.SQUARE_LENGTH,
            outline=draw.LIGHTGREY,
            width=5,
        )
    def deleteSquare(self):
        if self.squareHighlight:
            # canvas.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            canvas.canvas.delete(self.squareHighlight)
            self.squareHighlight = None
    def highlight(self, highlightType):
        self.highlighted = True
        self.drawCircle(highlightType)
        match highlightType:
            case HighlightType.Move:
                canvas.canvas.tag_bind(self.canvasObj, "<Button-1>", self.click)
            case HighlightType.Take:
                canvas.canvas.tag_bind(self.canvasObj, "<Button-1>", self.took)
                if self.piece:
                    self.piece.bindEvent("<Button-1>", self.took)
                    return
                self.bindEvent("<Button-1>", self.took)
    def unhighlight(self):
        self.highlighted = False
        if self.piece:
            canvas.canvas.tag_unbind(self.piece.imgObj, "<Button-1>")
            self.piece.bindEvent('<Button-1>', self.piece.select)
        self.deleteCircle()
    def took(self, e):
        board.takenBySelected(self)
    def color(self, color):
        canvas.canvas.itemconfig(self.id, fill=color, outline=color)

class Board(): # rows and columns start at 0, not 1
    def __init__(self, startPos):
        self.startPos = startPos
        self.board = self.createBoard(startPos)
        self.possibleMoves = []
        self.taken = {
            config.Color.black: [],
            config.Color.white: [],
        }
        self.selected = None
        self.lastHoveredOver = None
        # canvas.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
    def validate(self, boardPos, isTaking):
        arr = self.possibleMoves
        if isTaking:
            arr = self.possibleTakes
        for move in arr:
            if move.boardPos == boardPos:
                return True
        return False
    def movePiece(self, newSquare, piece, isTaking=False):
        if not self.validate(newSquare.boardPos, isTaking):
            return
        piece.square.setPiece(None)
        piece.snap(newSquare.boardPos)
        if piece.imgName == "pawn": # bad code but I'll only change it if another piece is like this
            piece.notMoved = False
            piece.canEnPassant = True
    def takePiece(self, piece):
        if not self.validate(piece.boardPos, True):
            return
        piece.deleteImg()
        self.taken[piece.color].append(piece)
        piece.square.setPiece(None)
    def moveSelected(self, boardPos):
        selected = self.selected
        square = self.getSquare(boardPos)
        self.unselect()
        self.movePiece(square, selected)
    def takenBySelected(self, square):
        selected = self.selected
        self.unselect()
        self.takePiece(square.piece)
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
    def createBoard(self, startPos):
        color = draw.BLACK
        board = []
        for row in range(config.BOARD_LENGTH):
            color = draw.switchColor(color)
            board.append([])
            for col in range(config.BOARD_LENGTH):
                boardPos = BoardPos(row, col)
                square = Square(self.getPosFromBoardPos(boardPos), boardPos, color)
                color = draw.switchColor(color)
                board[row].append(square)
        return board

def initBoard(startPos):
    global board
    board = Board(startPos)