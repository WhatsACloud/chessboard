import tkinter as tk

from pos import Pos
import canvas
import game
import config
import notification
from globals import globals

def main():
    globals.window = tk.Tk()
    globals.window.geometry(f"{config.WIDTH}x{config.HEIGHT}")
    # window.state('zoomed')
    canvas.initCanvas(globals.window)
    globals.game = game.Game(Pos(config.startX, config.startY), config.BOARD_LENGTH)
    # notification.Notification(" GAME END\nWHITE WINS")
    globals.window.mainloop()

if __name__ == "__main__":
    main()
