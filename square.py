import draw
import config
from globals import globals, HighlightType

class Square():
    def __init__(self, pos, boardPos, color):
        self.id = draw.drawSquare(pos, color)
        self.boardPos = boardPos
        self.origColor = color
        self.canvasObj = None
        self.highlighted = False
        self.squareHighlight = None
        self.pieceToTake = None # IF it is an available square to take (has circle on it), this is the piece that will be taken
        self.piece = None
        self.bindEvents()
    def bindEvent(self, evt, func):
        globals.canvas.tag_bind(self.id, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
    def enter(self):
        if globals.board.selected and globals.board.selected.dragging and not self.squareHighlight:
            self.drawSquare()
    def leave(self):
        self.deleteSquare()
    def setPiece(self, piece):
        self.piece = piece
    def click(self, e):
        if not self.highlighted:
            globals.board.unselect()
            return
        globals.board.moveSelected(self.boardPos)
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
        self.canvasObj = globals.canvas.create_oval(
            startPos.x + offset,
            startPos.y + offset,
            startPos.x + offset + circleLength,
            startPos.y + offset + circleLength,
            fill=fill,
            outline=draw.GREY,
            width=width
        )
    def deleteCircle(self):
        if self.canvasObj:
            # globals.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            globals.canvas.delete(self.canvasObj)
            self.canvasObj = None
    def drawSquare(self):
        startPos = globals.board.getPosFromBoardPos(self.boardPos)
        self.squareHighlight = globals.canvas.create_rectangle(
            startPos.x,
            startPos.y,
            startPos.x + config.SQUARE_LENGTH,
            startPos.y + config.SQUARE_LENGTH,
            outline=draw.LIGHTGREY,
            width=5,
        )
    def deleteSquare(self):
        if self.squareHighlight:
            # globals.canvas.tag_unbind(self.canvasObj, "<Button-1>")
            globals.canvas.delete(self.squareHighlight)
            self.squareHighlight = None
    def highlight(self, highlightType):
        self.highlighted = True
        self.drawCircle(highlightType)
        match highlightType:
            case HighlightType.Move:
                globals.canvas.tag_bind(self.canvasObj, "<Button-1>", self.click)
            case HighlightType.Take:
                globals.canvas.tag_bind(self.canvasObj, "<Button-1>", self.took)
                if self.piece:
                    self.piece.bindEvent("<Button-1>", self.took)
                    return
                self.bindEvent("<Button-1>", self.took)
    def unhighlight(self):
        self.highlighted = False
        self.pieceToTake = None
        if self.piece:
            globals.canvas.tag_unbind(self.piece.imgObj, "<Button-1>")
            self.piece.bindEvent('<Button-1>', self.piece.select)
        self.deleteCircle()
    def took(self, e=None):
        globals.board.takenBySelected(self)
    def color(self, color):
        globals.canvas.itemconfig(self.id, fill=color, outline=color)
