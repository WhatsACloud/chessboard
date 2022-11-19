import draw
import config
from globals import globals, HighlightType

class Square():
    def __init__(self, pos, boardPos, color):
        self.id = self.createObj(pos, color)
        self.boardPos = boardPos
        self.origColor = color
        self.canvasObj = None
        self.highlighted = False
        self.squareHighlight = None
        self.pieceToTake = None # IF it is an available square to take (has circle on it), this is the piece that will be taken
        self.piece = None
        self.after = None # my epiphany that I am stupid
        self.bindEvents()
    def delete(self):
        self.deleteSquare()
        self.deleteCircle()
        globals.canvas.canvas.delete(self.id)
        if self.piece:
            self.piece.delete()
    def __repr__(self):
        return f"[{self.boardPos.x}, {self.boardPos.y}]"
    def __hash__(self):
        return hash(self.boardPos)
    def runAfterFunc(self, piece):
        if self.after:
            self.after(piece)
            self.after = None
    def bindEvent(self, evt, func):
        globals.canvas.canvas.tag_bind(self.id, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
    def createObj(self, pos, color):
        startX, startY = pos.x, pos.y
        return globals.canvas.canvas.create_rectangle(
                startX,
                startY,
                startX + config.SQUARE_LENGTH,
                startY + config.SQUARE_LENGTH,
                outline=color,
                fill=color,
            )
    def enter(self):
        if globals.board.selected and globals.board.selected.dragging and not self.squareHighlight:
            self.drawSquare()
    def leave(self):
        self.deleteSquare()
    def setPiece(self, piece):
        self.piece = piece
    def click(self, e):
        if not self.highlighted:
            globals.board.unselectFully()
            return
        globals.board.moveSelected(self)
    def drawCircle(self, highlightType):
        startPos = globals.board.getPosFromBoardPos(self.boardPos)
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
        self.canvasObj = globals.canvas.canvas.create_oval(
            startPos.x + offset,
            startPos.y + offset,
            startPos.x + offset + circleLength,
            startPos.y + offset + circleLength,
            fill=fill,
            outline=draw.GREY,
            width=width
        )
    def moveto(self, pos):
        globals.canvas.canvas.moveto(self.id, pos.x, pos.y)
        if self.piece:
            self.piece.snap()
    def deleteCircle(self):
        if self.canvasObj:
            # globals.canvas.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            globals.canvas.canvas.delete(self.canvasObj)
            self.canvasObj = None
    def drawSquare(self):
        startPos = globals.board.getPosFromBoardPos(self.boardPos)
        self.squareHighlight = globals.canvas.canvas.create_rectangle(
            startPos.x,
            startPos.y,
            startPos.x + config.SQUARE_LENGTH,
            startPos.y + config.SQUARE_LENGTH,
            outline=draw.LIGHTGREY,
            width=5,
        )
    def deleteSquare(self):
        if self.squareHighlight:
            # globals.canvas.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            globals.canvas.canvas.delete(self.squareHighlight)
            self.squareHighlight = None
    def highlight(self, highlightType):
        self.highlighted = True
        self.drawCircle(highlightType)
        match highlightType:
            case HighlightType.Move:
                globals.canvas.canvas.tag_bind(self.canvasObj, "<Button-1>", self.click)
            case HighlightType.Take:
                globals.canvas.canvas.tag_bind(self.canvasObj, "<Button-1>", self.took)
                if self.piece:
                    self.piece.bindEvent("<Button-1>", self.took)
                    return
                self.bindEvent("<Button-1>", self.took)
    def unhighlight(self):
        self.highlighted = False
        self.pieceToTake = None
        if self.piece:
            globals.canvas.canvas.tag_unbind(self.piece.imgObj, "<Button-1>")
            self.piece.bindEvent('<Button-1>', self.piece.select)
        self.deleteCircle()
        self.after = None
    def took(self, e=None):
        globals.board.takenBySelected(self)
    def color(self, color):
        globals.canvas.canvas.itemconfig(self.id, fill=color, outline=color)
