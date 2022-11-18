import tkinter as tk
from PIL import Image, ImageTk

from pos import Pos, BoardPos
from globals import globals
from movesClass import Take, Move
import config
import draw
import copy

mouseX, mouseY = 0, 0

class PieceImg:
    def __init__(self, color, imgName):
        self.img = PieceImg.getImg(color, imgName)
        self.photoImg = ImageTk.PhotoImage(self.img, Image.ANTIALIAS)
        self.obj = None
        self.createObj()
    def bindEvent(self, evt, func):
        globals.canvas.canvas.tag_bind(self.obj, evt, func)
    def unbindEvent(self, evt):
        globals.canvas.canvas.tag_unbind(self.obj, evt)
    @staticmethod
    def getPieceImg(color, imgName):
        return f"assets/{color}_{imgName}.png"
    @staticmethod
    def getImg(color, imgName):
        # img = tk.PhotoImage(file=PieceImg.getPieceImg(color, imgName))
        img = Image.open(PieceImg.getPieceImg(color, imgName))
        return img
    def createObj(self):
        if self.obj:
            globals.canvas.canvas.delete(self.obj)
        self.obj = globals.canvas.canvas.create_image(
            50,
            50,
            image=self.photoImg,
        )
        globals.canvas.canvas.moveto(self.obj, 50, 50)
    def hide(self):
        globals.canvas.canvas.delete(self.obj)
    def resize(self, width):
        self.img = self.img.resize((width, width))
        self.photoImg = ImageTk.PhotoImage(self.img, Image.ANTIALIAS)
        self.createObj()
    def move(self, amt):
        globals.canvas.canvas.move(self.obj, amt.x, amt.y)
    def moveto(self, pos):
        globals.canvas.canvas.moveto(self.obj, pos.x, pos.y)
    def delete(self):
        self.hide()
        self.img = None
        self.photoImg = None
        self.obj = None

class Piece():
    def __init__(self, boardPos, color):
        self.boardPos = boardPos
        self.imgObj = PieceImg(color, self.imgName)
        self.square = globals.board.getSquare(boardPos)
        self.dragging = False
        self.color = color
        self.updateBoard()
        self.snap()
        self.bindEvents()
        globals.board.pieces[self.color].append(self)
    def remove(self):
        self.delete()
        globals.board.taken.add(self)
        globals.board.pieces[self.color].remove(self)
    def delete(self):
        self.deleteImg()
        self.square.setPiece(None)
    def deleteImg(self):
        self.imgObj.hide()
    def updateBoard(self):
        globals.board.getSquare(self.boardPos).piece = self
    def unselect(self):
        self.square.color(self.square.origColor)
    def getMoves(self):
        moves = set()
        takes = set()
        for move in self.moves:
            # if self.imgName == "king":
            newMoves = move.calc(self)
            moves = moves | newMoves
        for take in self.takes:
            square = take.calc(self)
            if square:
                takes.add(square)
        return moves, takes
    def setMoves(self, moves, takes=None):
        self.moves = moves
        if takes:
            for take in takes:
                if type(take) != Take:
                    raise Exception('Takes array had object of type Move')
        if takes == None:
            takes = []
            for move in self.moves:
                takes.append(Take([direction for direction in move.directions], cond=move.cond, amt=move.amt))
        self.takes = takes
        otherColor = config.changeColor(self.color)
        attackAngles = []
        for take in takes:
            attackAngles.append(Take([direction * -1 for direction in take.directions], cond=take.cond, amt=take.amt))
        globals.attackAngles[otherColor][type(self)] = attackAngles # reverses direction
    def moveto(self, boardPos):
        self.square.setPiece(None)
        self.square = globals.board.getSquare(boardPos)
        self.boardPos = boardPos
        self.square.setPiece(self)
    def snap(self, boardPos=None):
        if boardPos == None:
            boardPos = self.boardPos
        self.movetoPos(globals.board.getPosFromBoardPos(boardPos))
        self.moveto(boardPos)
        self.dragging = False
    def bindEvent(self, event, func):
        self.imgObj.bindEvent(event, func)
    def bindEvents(self):
        self.bindEvent('<Button1-Motion>', self.drag)
        self.bindEvent('<Button1-ButtonRelease>', self.drop)
        self.bindEvent('<Button-1>', self.select)
    def reset(self):
        self.unselect()
        globals.board.unhighlight()
        self.snap()
    def drop(self, e):
        if globals.board.lastHoveredOver:
            globals.board.lastHoveredOver.leave()
        globals.board.lastHoveredOver = None

        global mouseX, mouseY
        mouseX, mouseY = 0, 0

        if not self.dragging:
            return
        if not globals.board.isCorrectColor(self):
            return self.snap()
        pos = Pos(e.x, e.y)
        square = globals.board.getSquareWhichPosInside(pos)
        if square == None:
            return self.reset()
        if square and square.piece:
            if self.color != square.piece.color:
                return square.took()
            return self.reset()
        globals.board.moveSelected(square)
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
        self.imgObj.move(Pos(moveX, moveY))
        
        square = globals.board.getSquareWhichPosInside(Pos(mouseX, mouseY))
        if not square or globals.board.lastHoveredOver == square:
            return
        if globals.board.lastHoveredOver:
            globals.board.lastHoveredOver.leave()
        square.enter()
        globals.board.lastHoveredOver = square
        # globals.canvas.canvas.moveto(self.imgObj, x, y)
    def movetoPos(self, pos):
        self.imgObj.moveto(pos)
    def select(self, e):
        globals.board.select(self)
