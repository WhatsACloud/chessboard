import tkinter as tk
import types

from pos import Pos, BoardPos
from board import getBoard
import canvas
import draw
import copy
from movesClass import Direction, Move

mouseX, mouseY = 0, 0

class Color():
    black = "black"
    white = "white"

class PieceImg(): # display
    def __init__(self, color, piece): # where piece is the parent class
        self.img = tk.PhotoImage(file=PieceImg.getPieceImg(color, piece.imgName))
        self.imgObj = canvas.canvas.create_image(60, 60, image=self.img)
        self.piece = piece
        self.square = getBoard().getSquare(piece.boardPos)
        self.bindEvents()
    def bindEvent(self, event, func):
        canvas.canvas.tag_bind(self.imgObj, event, func)
    def bindEvents(self):
        pass
        # self.bindEvent('<Button1-Motion>', self.drag)
        # self.bindEvent('<Button1-ButtonRelease>', self.drop)
        self.bindEvent('<Button-1>', self.select)
    # def drop(self, e):
        # global mouseX, mouseY
        # mouseX, mouseY = 0, 0
        # pos = Pos(e.x, e.y)
        # square = self.piece.board.getSquareWhichPosInside(pos)
        # if square:
            # self.piece.boardPos = square
        # self.piece.snap()
    # def drag(self, e):
        # global mouseX, mouseY
        # x, y = e.x, e.y
        # moveX = x - mouseX
        # moveY = y - mouseY
        # if mouseX == 0 or mouseY == 0:
            # moveX = 0
            # moveY = 0
        # mouseX, mouseY = x, y
        # canvas.canvas.move(self.imgObj, moveX, moveY)
        # canvas.canvas.moveto(self.imgObj, x, y)
    def moveto(self, pos):
        canvas.canvas.moveto(self.imgObj, pos.x, pos.y)
    def select(self, e):
        getBoard().select(self.piece)
    @staticmethod
    def getPieceImg(color, imgName):
        return f"assets/{color}_{imgName}.png"

class Piece():
    def __init__(self, boardPos, color):
        self.boardPos = boardPos
        self.pieceImg = PieceImg(color, self)
        self.color = color
        self.updateBoard()
        self.snap()
    def updateBoard(self):
        getBoard().getSquare(self.boardPos).piece = self
    def unselect(self):
        self.pieceImg.square.color(self.pieceImg.square.origColor)
    def getMoves(self):
        moves = []
        for move in self.moves:
            moves += move.calc(self.boardPos)
        return moves
    def setMoves(self, moves):
        self.moves = moves
    def snap(self, boardPos=None):
        if boardPos == None:
            boardPos = self.boardPos
        self.pieceImg.moveto(getBoard().getPosFromBoardPos(boardPos))
        self.pieceImg.square = getBoard().getSquare(boardPos)
        self.boardPos = boardPos
        self.pieceImg.square.piece = self

class Rook(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "rook"
        super().__init__(boardPos, color)
        self.setMoves([
            Move([Direction.up]),
            Move([Direction.down]),
            Move([Direction.left]),
            Move([Direction.right]),
        ])

class Bishop(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "bishop"
        super().__init__(boardPos, color)
        self.setMoves([
            Move([Direction.up, Direction.left]),
            Move([Direction.left, Direction.down]),
            Move([Direction.down, Direction.right]),
            Move([Direction.right, Direction.up]),
        ])

class Pawn(Piece):
    def __init__(self, boardPos, color):
        self.imgName = "pawn"
        super().__init__(boardPos, color)
        self.moved = False
        self.setMoves()
