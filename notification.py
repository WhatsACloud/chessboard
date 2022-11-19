import tk
from globals import globals
from pos import Scale, Pos
import draw
import canvasObjs

# WIDTH, HEIGHT = 400, 120
bgDim = Scale(0.3, 0.2)
textDim = Scale(0.1, 0.05)
buttonSize = textDim + Scale(0.02, 0.02)
defaultFontSize = 12

class Notification:
    def __init__(self, text):
        # self.background = globals.canvas.canvas.create_rectangle(0, 0, 0, 0, fill="grey", outline="white")
        self.background = canvasObjs.Rect(globals.canvas.centerOf(bgDim), bgDim, fill="grey", outline="white")
        self.text = canvasObjs.Text(None, defaultFontSize, text, centerPoint=Scale(0.5, 0.5))
        buttonPos = globals.canvas.centerOf(buttonSize, self.background.center)
        buttonPos.y += self.background.size.y/2 - buttonSize.y/2 - 0.01
        self.button = canvasObjs.Button(
            self.close,
            buttonPos,
            buttonSize,
            draw.RED,
            draw.DARKRED,
            defaultFontSize,
            "restart game"
        )
        globals.canvas.bindToResize(self.update)
        self.update()
    def delete(self):
        self.background.delete()
        self.text.delete()
        self.button.delete()
    def close(self, e):
        self.delete()
        globals.canvas.unbindResize(self.update)
        globals.game.reset()
    def update(self):
        self.background.update()
        self.text.update()
        self.button.update()
