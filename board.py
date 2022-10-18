# Note: board array should be rows of columns
import draw
import math
from pos import BoardPos, Pos
import config
import canvas

board = None

def getBoard():
    return board

class Square():
    def __init__(self, pos, boardPos, color):
        self.id = draw.drawSquare(pos, color)
        self.boardPos = boardPos
        self.origColor = color
        self.piece = None
        self.bindEvents()
    def bindEvents(self):
        canvas.canvas.tag_bind(self.id, "<Button-1>", self.click)
    def click(self, e):
        global board
        board.unselect()
    def color(self, color):
        canvas.canvas.itemconfig(self.id, fill=color, outline=color)

class Board(): # rows and columns start at 0, not 1
    def __init__(self, startPos):
        self.startPos = startPos
        self.board = self.getBoard(startPos)
        self.selected = None
        # canvas.canvas.bind("<Button-1>", self.click)
        # self.drawnBoard = draw.drawBoard(canvas, boardLength, config.SQUARE_LENGTH, startPos)
    def unselect(self):
        if self.selected:
            self.selected.unselect()
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
    def getBoard(self, startPos):
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
