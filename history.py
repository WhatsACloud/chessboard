from globals import globals
import config

class HistoryItem:
    def __init__(self, prev, origin, to, pieceTaken=None, after=None):
        self._next = None # as in history item
        self.prev = prev # as in history item
        self.after = after
        self.origin = origin
        self.to = to
        self.forwarded = False
        self.pieceTaken = pieceTaken
    def reverseAfterFunc(self, piece):
        if self.after:
            self.after.reverse(piece)
    def afterFunc(self, piece):
        if self.after:
            self.after.after(piece)
    @property
    def next(self):
        return self._next
    @next.setter
    def next(self, nextItem):
        self._next = nextItem
    def back(self):
        to = globals.board.getSquare(self.to)
        origin = globals.board.getSquare(self.origin)
        piece = to.piece
        self.reverseAfterFunc(piece)
        piece = to.piece
        print(piece, self.origin, to)
        piece.moveto(self.origin)
        if self.pieceTaken:
            self.pieceTaken.reAdd(to)
            self.pieceTaken.snap()
        # origin.piece.snap()
        globals.turn = config.changeColor(globals.turn)
        globals.board.reverseBoard()
    def forward(self):
        if self.pieceTaken:
            globals.board.takePiece(self.pieceTaken)
        globals.board.movePiece(self.to.boardPos, self.origin.piece)
        self.afterFunc(self.to.piece)

class Base:
    def __init__(self):
        self.next = None
        self.prev = None

class History:
    def __init__(self):
        self.current = Base()
    def add(self, origin, to, pieceTaken=None, after=None):
        new = HistoryItem(self.current, origin, to, pieceTaken, after)
        if self.current.next:
            self.current.next.prev = None
        self.current.next = new
        self.current = new
    def back(self, amt=1):
        for _ in range(amt):
            globals.board.decrementCurrentIndex()
            if not self.current.prev:
                return
            self.current.forwarded = False
            self.current.back()
            self.current = self.current.prev
    def forward(self, amt=1):
        for _ in range(amt):
            globals.board.incrementCurrentIndex()
            if not self.current.next:
                if not self.current.forwarded:
                    self.current.forwarded = True
                    self.current.forward()
                return
            self.current.forward()
            self.current = self.current.next
