import tkinter as tk

from pos import Pos
import canvas
import game
import config
import notification

def main():
    window = tk.Tk()
    window.geometry(f"{config.WIDTH}x{config.HEIGHT}")
    # window.state('zoomed')
    canvas.initCanvas(window)
    game.Game(Pos(config.startX, config.startY), config.BOARD_LENGTH)
    notification.Notification(" GAME END\nWHITE WINS")
    window.mainloop()

if __name__ == "__main__":
    main()
