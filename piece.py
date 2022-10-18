import tkinter as tk
import types

from pos import Pos, BoardPos
from board import getBoard
import canvas
import draw
import copy
from moves import Direction, Move

class PieceConfig():
    def __init__(self, moves, imgName):
        self.imgName = imgName
        self.moves = moves
    def getMoves(self):
        moves = []
        for move in self.moves:
            move.calc(boardPos)

class pieceTypes(): # basically an enum BUUUUUUUT it also stores the image name lol
    blackBishop = "black_bishop"
    whiteBishop = "white_bishop"
    blackKnight = "black_knight"
    whiteKnight = "white_knight"
    blackKing = "black_king"
    whiteKing = "white_king"
    blackQueen = "black_queen"
    whiteQueen = "white_queen"
    blackRook = "black_rook"
    whiteRook = "white_rook"

def getPieceImg(imgName):
    return f"assets/{imgName}.png"

mouseX, mouseY = 0, 0

class PieceImg(): # display
    def __init__(self, pieceType, piece): # where piece is the parent class
        self.img = tk.PhotoImage(file=getPieceImg(pieceType))
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
    def snap(self):
        self.moveto(getBoard().getPosFromBoardPos(self.piece.boardPos))
    def unselect(self):
        getBoard().selected = None
        self.square.color(self.square.origColor)
    def select(self, e):
        getBoard().unselect()
        getBoard().selected = self
        self.square.color(draw.ORANGE)
        print(getBoard().selected)

class Piece():
    def __init__(self, pieceType, boardPos):
        self.boardPos = boardPos
        self.pieceImg = PieceImg(pieceType, self)
        self.updateBoard()
    def updateBoard(self):
        getBoard().getSquare(self.boardPos).piece = self
    def getMoves(self):
        moves = []
        for move in self.moves:
            moves += move.calc(boardPos)
        return moves
    def setMoves(self, moves):
        self.moves = moves

class Rook(Piece):
    def __init__(self, pieceType, boardPos):
        super().__init__(pieceType, boardPos)
        self.setMoves([
            Move([Direction.up]),
            Move([Direction.down]),
            Move([Direction.left]),
            Move([Direction.right]),
        ])

class Pawn(Piece):
    def __init__(self, pieceType, boardPos):
        super().__init__(pieceType, boardPos)
        self.moved = False
        self.setMoves()
