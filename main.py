import tkinter as tk

import board as bd
from pos import Pos, BoardPos
import piece
import canvas
import config

def main():
    window = tk.Tk()
    window.geometry(f"{config.WIDTH}x{config.HEIGHT}")
    window.state('zoomed')
    canvas.initCanvas(window)
    bd.initBoard(Pos(config.startX, config.startY))

    test = piece.Rook(BoardPos(4, 4), piece.Color.white)
    test2 = piece.Bishop(BoardPos(3, 3), piece.Color.white)
    window.mainloop()

if __name__ == "__main__":
    main()
