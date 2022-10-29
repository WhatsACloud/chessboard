import tkinter as tk
import types

from pos import Pos, BoardPos
from globals import globals
from movesClass import Take, Move
import draw
import copy

mouseX, mouseY = 0, 0

class Piece():
    def __init__(self, boardPos, color):
        self.boardPos = boardPos
        self.img = tk.PhotoImage(file=Piece.getPieceImg(color, self.imgName))
        self.imgObj = None
        self.drawImg()
        self.square = globals.board.getSquare(boardPos)
        self.dragging = False
        self.bindEvents()
        self.color = color
        self.updateBoard()
        self.snap()
    def drawImg(self):
        self.imgObj = globals.canvas.create_image(60, 60, image=self.img)
    def deleteImg(self):
        globals.canvas.delete(self.imgObj)
        self.imgObj = None
    def updateBoard(self):
        globals.board.getSquare(self.boardPos).piece = self
    def unselect(self):
        self.square.color(self.square.origColor)
    def getMoves(self):
        moves = []
        takes = []
        for move in self.moves:
            newMoves = move.calc(self)
            moves += newMoves
        for take in self.takes:
            newTakes = take.calc(self)
            takes += newTakes
        moves = list(set(moves))
        takes = list(set(takes))
        return moves, takes
    def setMoves(self, moves, takes=None):
        self.moves = moves
        if takes == None:
            self.takes = []
            for move in self.moves:
                self.takes.append(Take(move.directions, cond=move.cond, amt=move.amt))
            return
        self.takes = takes
    def snap(self, boardPos=None):
        if boardPos == None:
            boardPos = self.boardPos
        self.movetoPos(globals.board.getPosFromBoardPos(boardPos))
        self.square = globals.board.getSquare(boardPos)
        self.boardPos = boardPos
        self.square.setPiece(self)
        self.dragging = False
    def bindEvent(self, event, func):
        globals.canvas.tag_bind(self.imgObj, event, func)
    def bindEvents(self):
        self.bindEvent('<Button1-Motion>', self.drag)
        self.bindEvent('<Button1-ButtonRelease>', self.drop)
        self.bindEvent('<Button-1>', self.select)
    def drop(self, e):
        if not self.dragging:
            return
        global mouseX, mouseY
        mouseX, mouseY = 0, 0
        pos = Pos(e.x, e.y)
        square = globals.board.getSquareWhichPosInside(pos)
        if square and square.piece:
            square.took()
        else:
            globals.board.moveSelected(square.boardPos)
        self.snap()
        if globals.board.lastHoveredOver:
            globals.board.lastHoveredOver.leave()
        globals.board.lastHoveredOver = None
    def drag(self, e):
        self.dragging = True
        global mouseX, mouseY
        x, y = e.x, e.y
        moveX = x - mouseX
        moveY = y - mouseY
        if mouseX == 0 or mouseY == 0:
            moveX = 0
            moveY = 0
        mouseX, mouseY = x, y
        globals.canvas.move(self.imgObj, moveX, moveY)
        
        square = globals.board.getSquareWhichPosInside(Pos(mouseX, mouseY))
        if not square or globals.board.lastHoveredOver == square:
            return
        if globals.board.lastHoveredOver:
            globals.board.lastHoveredOver.leave()
        square.enter()
        globals.board.lastHoveredOver = square
        # globals.canvas.moveto(self.imgObj, x, y)
    def movetoPos(self, pos):
        globals.canvas.moveto(self.imgObj, pos.x, pos.y)
    def select(self, e):
        globals.board.select(self)
    @staticmethod
    def getPieceImg(color, imgName):
        return f"assets/{color}_{imgName}.png"
