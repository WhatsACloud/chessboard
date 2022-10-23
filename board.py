# Note: board array should be rows of columns
import draw
import math
from pos import BoardPos, Pos
import config
import canvas

"""
for sake of simplicity:
    Board starts at top left, which is the side where black is
"""

board = None

def getBoard():
    return board

class Square():
    def __init__(self, pos, boardPos, color):
        self.id = draw.drawSquare(pos, color)
        self.boardPos = boardPos
        self.origColor = color
        self.circle = None
        self.highlighted = False
        self.piece = None
        self.bindEvents()
    def bindEvent(self, evt, func):
        canvas.canvas.tag_bind(self.id, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
    def click(self, e):
        if not self.highlighted:
            board.unselect()
            return
        board.moveSelected(self.boardPos)
    def createCircle(self):
        pos = board.getPosFromBoardPos(self.boardPos)
        circleLength = config.SQUARE_LENGTH / 4
        offset = config.SQUARE_LENGTH / 2 - circleLength / 2
        self.circle = canvas.canvas.create_oval(
            pos.x + offset,
            pos.y + offset,
            pos.x + offset + circleLength,
            pos.y + offset + circleLength,
            fill=draw.GREY,
            outline=draw.GREY,
        )
        canvas.canvas.tag_bind(self.circle, "<Button-1>", self.click)
    def deleteCircle(self):
        if self.circle:
            canvas.canvas.tag_unbind(self.circle, "<Button-1>")
            canvas.canvas.delete(self.circle)
            self.circle = None
    def highlight(self):
        self.highlighted = True
        self.createCircle()
    def unhighlight(self):
        self.highlighted = False
        self.deleteCircle()
    def color(self, color):
        canvas.canvas.itemconfig(self.id, fill=color, outline=color)

class Board(): # rows and columns start at 0, not 1
    def __init__(self, startPos):
        self.startPos = startPos
        self.board = self.createBoard(startPos)
        self.possibleMoves = []
        self.selected = None
        # canvas.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
    def validate(self, boardPos, selected):
        for move in self.possibleMoves:
            if move.boardPos == boardPos:
                return True
        return False
    def movePiece(self, newSquare, piece):
        if not self.validate(newSquare.boardPos, piece):
            return
        piece.square.piece = None
        piece.snap(newSquare.boardPos)
        if piece.imgName == "pawn": # very bad code but I'll only change it if another piece is like this
            piece.notMoved = False
    def moveSelected(self, boardPos):
        selected = self.selected
        square = self.getSquare(boardPos)
        self.unselect()
        self.movePiece(square, selected)
    def select(self, piece):
        self.unselect()
        self.selected = piece
        piece.square.color(draw.ORANGE)
        self.possibleMoves = piece.getMoves()
        for square in self.possibleMoves:
            square.highlight()
    def unselect(self):
        if self.selected:
            self.selected.unselect()
            for square in self.possibleMoves:
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