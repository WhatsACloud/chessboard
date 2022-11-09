import tkinter as tk
import types

from pos import Pos, BoardPos
from globals import globals
from movesClass import Take, Move
import config
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
        self.color = color
        self.updateBoard()
        self.snap()
    @staticmethod
    def getImg(color, imgName):
        img = tk.PhotoImage(file=Piece.getPieceImg(color, imgName))
        return img
    def getImgObj(img):
        imgObj = globals.canvas.canvas.create_image(
            config.SQUARE_LENGTH,
            config.SQUARE_LENGTH,
            image=img
        )
        return imgObj
    def drawImg(self):
        self.imgObj = globals.canvas.canvas.create_image(config.SQUARE_LENGTH, config.SQUARE_LENGTH, image=self.img)
        self.bindEvents()
    def delete(self):
        self.deleteImg()
        globals.board.taken[self.color].append(self)
    def deleteImg(self):
        globals.canvas.canvas.delete(self.imgObj)
        self.imgObj = None
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
            newTakes = take.calc(self)
            takes = takes | newTakes
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
        otherColor = config.Color.white
        if self.color == otherColor:
            otherColor = config.Color.black
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
        globals.canvas.canvas.tag_bind(self.imgObj, event, func)
    def bindEvents(self):
        self.bindEvent('<Button1-Motion>', self.drag)
        self.bindEvent('<Button1-ButtonRelease>', self.drop)
        self.bindEvent('<Button-1>', self.select)
    def drop(self, e):
        global mouseX, mouseY
        mouseX, mouseY = 0, 0
        if not globals.board.isCorrectColor(self):
            self.snap()
            return
        if not self.dragging:
            return
        pos = Pos(e.x, e.y)
        square = globals.board.getSquareWhichPosInside(pos)
        if square == None:
            return
        if square and square.piece:
            square.took()
        else:
            globals.board.moveSelected(square)
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
        globals.canvas.canvas.move(self.imgObj, moveX, moveY)
        
        square = globals.board.getSquareWhichPosInside(Pos(mouseX, mouseY))
        if not square or globals.board.lastHoveredOver == square:
            return
        if globals.board.lastHoveredOver:
            globals.board.lastHoveredOver.leave()
        square.enter()
        globals.board.lastHoveredOver = square
        # globals.canvas.canvas.moveto(self.imgObj, x, y)
    def movetoPos(self, pos):
        globals.canvas.canvas.moveto(self.imgObj, pos.x, pos.y)
    def select(self, e):
        globals.board.select(self)
    @staticmethod
    def getPieceImg(color, imgName):
        return f"assets/{color}_{imgName}.png"
