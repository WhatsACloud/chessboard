import tkinter as tk
from globals import globals

class Canvas: # why james WHY
    def __init__(self, canvasWidget):
        self.canvas = canvasWidget
    def getDimensions(self):
        return [self.canvas.winfo_width(), self.canvas.winfo_height()]

def initCanvas(window): # there's probably a better way to do this
    canvas = tk.Canvas(window, width=800, height=600, bg='steelblue')
    canvas.pack(fill=tk.BOTH, expand=True)
    globals.canvas = Canvas(canvas)
