import tkinter as tk
from pos import BoardPos
from globals import globals
import config
import pieces
import draw
from piece import Piece
canvas, board = globals.canvas, globals.board

pieces = { # name of images of pieces that can pawn can promote to
    pieces.Queen,
    pieces.Bishop,
    pieces.Knight,
    pieces.Rook,
}

class PromotionPiece:
    def __init__(self, square, piece, promotingPawn, pieceType, prompt, newSquare):
        self.square = square
        self.piece = piece
        self.toMoveTo = newSquare
        self.promotingPawn = promotingPawn
        self.pieceType = pieceType
        self.prompt = prompt
        self.bindEvents()
    def click(self, e):
        self.promotingPawn.snap(self.toMoveTo)
        globals.board.nextTurn()
        square = self.promotingPawn.square
        color = self.promotingPawn.color
        self.promotingPawn.delete()
        self.pieceType(square.boardPos, color)
        self.prompt.delete()
        self.prompt = None
    def bindEvent(self, event, func):
        globals.canvas.tag_bind(self.piece, event, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)

class PromotionPrompt:
    def __init__(self, boardPos, color, newSquare):
        self.squares = []
        self.imgs = []
        increment = BoardPos(0, -1)
        self.promotingPawn = globals.board.getSquare(boardPos).piece
        if color == config.Color.white:
            increment *= -1
        for pieceType in pieces:
            startPos = globals.board.getPosFromBoardPos(newSquare)
            square = self.drawSquare(startPos)
            imgObj, img = pieceType.getImg(color, pieceType.imgName)
            self.imgs.append(img)
            globals.canvas.moveto(imgObj, startPos.x, startPos.y)
            self.squares.append(PromotionPiece(square, imgObj, self.promotingPawn, pieceType, self, newSquare))
            newSquare += increment
        self.funcId = globals.canvas.bind("<ButtonRelease-1>", self.release)
    def release(self, e):
        globals.canvas.unbind("<ButtonRelease-1>", self.funcId)
        self.funcId = globals.canvas.bind("<Button-1>", self.cancel)
    def cancel(self, e):
        globals.canvas.unbind("<Button-1>", self.funcId)
        self.delete()
    def delete(self):
        for square in self.squares:
            globals.canvas.delete(square.square)
            globals.canvas.delete(square.piece)
    def drawSquare(self, startPos):
        return globals.canvas.create_rectangle(
            startPos.x,
            startPos.y,
            startPos.x + config.SQUARE_LENGTH,
            startPos.y + config.SQUARE_LENGTH,
            outline=draw.WHITE,
            fill=draw.WHITE,
            width=5,
        )
