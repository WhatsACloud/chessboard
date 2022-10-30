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
    def __init__(self, square, piece, promotingPawn, pieceType, prompt):
        self.square = square
        self.piece = piece
        self.promotingPawn = promotingPawn
        self.pieceType = pieceType
        self.prompt = prompt
    def click(self, e):
        square = self.promotingPawn.square
        color = self.promotingPawn.color
        self.promotingPawn.delete()
        self.pieceType(square.boardPos, color)
        self.prompt.delete()
        self.prompt = None
    def bindEvent(self, event, func):
        globals.canvas.tag_bind(self.piece, event, func)
    def bindEvents(self):
        pass

class PromotionPrompt:
    def __init__(self, boardPos, color):
        self.squares = []
        self.imgs = []
        increment = BoardPos(0, -1)
        if color == config.Color.white:
            increment *= -1
        for pieceType in pieces:
            startPos = globals.board.getPosFromBoardPos(boardPos)
            square = self.drawSquare(startPos)
            imgObj, img = pieceType.getImg(color)
            self.imgs.append(img)
            globals.canvas.moveto(imgObj, startPos.x, startPos.y)
            self.squares.append(PromotionPiece(square, imgObj, promotingPawn, pieceType, self))
            boardPos += increment
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
