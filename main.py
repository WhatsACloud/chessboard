import tkinter as tk

import board as bd
from pos import Pos, BoardPos
import pieces
import piece
import canvas
import config

def setupPieces(color):
    firstRow, secondRow = None, None
    end = config.BOARD_LENGTH-1
    if color == piece.Color.black:
        firstRow, secondRow = 0, 1
    else:
        firstRow, secondRow = end, end-1
    pieces.Rook(BoardPos(0, firstRow), color)
    pieces.Rook(BoardPos(end, firstRow), color)
    pieces.Knight(BoardPos(1, firstRow), color)
    pieces.Knight(BoardPos(end-1, firstRow), color)
    pieces.Bishop(BoardPos(2, firstRow), color)
    pieces.Bishop(BoardPos(end-2, firstRow), color)
    pieces.Queen(BoardPos(3, firstRow), color)
    pieces.King(BoardPos(end-3, firstRow), color)
    for i in range(config.BOARD_LENGTH):
        pieces.Pawn(BoardPos(i, secondRow), color)

def main():
    window = tk.Tk()
    window.geometry(f"{config.WIDTH}x{config.HEIGHT}")
    window.state('zoomed')
    canvas.initCanvas(window)
    bd.initBoard(Pos(config.startX, config.startY))

    setupPieces(piece.Color.black)
    setupPieces(piece.Color.white)
    window.mainloop()

if __name__ == "__main__":
    main()