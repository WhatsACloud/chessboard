import tkinter as tk
from pos import Pos, Scale
from globals import globals

class Canvas: # why james WHY
    def __init__(self, canvasWidget):
        self.canvas = canvasWidget
        self.screenSize = self.getScreenSize()
        self.resizeEvts = []
    def getDimensions(self):
        self.canvas.update()
        return Pos(self.canvas.winfo_width(), self.canvas.winfo_height())
    def getScreenSize(self):
        return Pos(self.canvas.winfo_screenwidth(), self.canvas.winfo_screenheight())
    def getFontSizeFromScale(self, size):
        return int(size * self.getDimensions().x)
    def toScale(self, scale):
        dimensions = self.getDimensions()
        return Pos(dimensions.x * scale.x, dimensions.y * scale.y)
    def centerOf(self, scale, center=None): # get start of centered element given its relative width and height
        if center == None:
            center = Scale(0.5, 0.5) # center of screen
        return Scale(center.x - scale.x / 2, center.y - scale.y / 2)
    def bindToResize(self, func):
        self.resizeEvts.append(func)
    def resize(self, e):
        for evt in self.resizeEvts:
            evt()

def initCanvas(window):
    canvas = tk.Canvas(window, width=800, height=600, bg='steelblue')
    canvas.pack(fill=tk.BOTH, expand=True)
    globals.canvas = Canvas(canvas)
    window.bind("<Configure>", globals.canvas.resize)
