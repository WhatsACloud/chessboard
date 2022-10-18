import tkinter as tk

import board as bd
from pos import Pos, BoardPos
import piece
import canvas
import config

def main():
    window = tk.Tk()
    window.geometry(f"{config.WIDTH}x{config.HEIGHT}")
    canvas.initCanvas(window)
    bd.initBoard(Pos(config.startX, config.startY))

    test = piece.Piece(piece.pieceTypes.whiteBishop, BoardPos(0, 0))
    test.snap()
    window.mainloop()

if __name__ == "__main__":
    main()
