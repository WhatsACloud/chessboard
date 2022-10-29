import tkinter as tk
from globals import globals

def initCanvas(window): # there's probably a better way to do this
    canvas = tk.Canvas(window, width=800, height=600, bg='steelblue')
    canvas.pack(fill=tk.BOTH, expand=True)
    globals.canvas = canvas
