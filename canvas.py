import tkinter as tk

canvas = None

def initCanvas(window): # there's probably a better way to do this
    global canvas
    canvas = tk.Canvas(window, width=800, height=600, bg='steelblue')
    canvas.pack(fill=tk.BOTH, expand=True)
