try:
    import tkinter as tk
except ImportError: # python2
    import Tkinter as tk
from pos import Pos, Scale
from globals import globals

class Canvas: # why james WHY
    def __init__(self, canvasWidget):
        self.canvas = canvasWidget
        self.resizeEvts = []
    def getDimensions(self):
        # return Pos(self.canvas.winfo_width(), self.canvas.winfo_height())
        pos = Pos(globals.window.winfo_width(), globals.window.winfo_height())
        return pos
    def getScaleFromFontSize(self, size): # returns relative i.e. betw. 1 and 0 size based on font size and screen size proportions
        return size / 1000
    def toActual(self, scale):
        dimensions = self.getDimensions()
        return Pos(dimensions.x * scale.x, dimensions.y * scale.y)
    def toScale(self, pos):
        dimensions = self.getDimensions()
        return Scale(pos.x / dimensions.x, pos.y / dimensions.y)
    def centerOf(self, scale, center=None): # get start of centered element given its relative width and height
        if center == None:
            center = Scale(0.5, 0.5) # center of screen
        return Scale(center.x - scale.x / 2, center.y - scale.y / 2)
    def bindToResize(self, func):
        self.resizeEvts.append(func)
    def resize(self, e):
        for evt in self.resizeEvts:
            evt()
    def unbindResize(self, func):
        self.resizeEvts.remove(func)
    def unbindAllResize(self):
        self.resizeEvts = []
    def delete(self):
        self.unbindAllResize()
        self.canvas.destroy()

def initCanvas(window):
    canvas = tk.Canvas(window, width=800, height=600, bg='steelblue')
    canvas.pack(fill=tk.BOTH, expand=True)
    if globals.canvas:
        globals.canvas.delete()
        del globals.canvas
    globals.canvas = Canvas(canvas)
    window.bind("<Configure>", globals.canvas.resize)
