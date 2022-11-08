import tk
from globals import globals
from pos import Scale, Pos
import draw
import config
import math
from abc import ABC, abstractmethod

# WIDTH, HEIGHT = 400, 120
bgDim = Scale(0.3, 0.2)
textDim = Scale(0.15, 0.1)
fontSize = 0.01

class AbsObj(ABC):
    def __init__(self, scale=None, size=None, offset=None):
        if scale == None:
            scale = Scale(0, 0)
        if size == None:
            size = Scale(0, 0)
        if offset == None:
            offset = Pos(0, 0)
        self.scale = scale
        self.size = size
        self.offset = offset
        self.obj = self.createObj()

    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def createObj(self):
        pass
    @abstractmethod
    def getSize(self):
        pass
    def getPos(self):
        return globals.canvas.toScale(self.scale)
    def delete(self):
        globals.canvas.canvas.delete(self.obj)
    @property
    def end(self):
        return globals.canvas.toScale(self.scale + self.size)
    def actual(self, scale):
        return globals.canvas.toScale(scale)

class Rect(AbsObj):
    def __init__(self, scale, size, fill, activeFill=None, offset=None, outline=None):
        if outline == None:
            outline = fill
        self.color = fill
        self.activeColor = activeFill
        self.outline = outline
        super().__init__(scale, size, offset)
    def createObj(self):
        return globals.canvas.canvas.create_rectangle(
            self.actual(self.scale).x,
            self.actual(self.scale).y,
            self.end.x,
            self.end.y,
            fill=self.color,
            activefill=self.activeColor,
            outline=self.outline
        )
    def update(self):
        globals.canvas.canvas.coords(self.obj, self.actual(self.scale).x, self.actual(self.scale).y, self.end.x, self.end.y)
    def getSize(self):
        return self.size

class Text(AbsObj):
    def __init__(self, size, text, offset=None, color=draw.BLACK):
        self._text = text
        self.color = color
        super().__init__(None, size, offset)
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, text):
        self._text = text
        globals.canvas.canvas.itemconfig(text, text=text)
    @property
    def actualSize(self):
        return math.ceil(self.size * globals.canvas.getDimensions().x)
    def createObj(self): # because yes
        pos = self.getPos()
        return globals.canvas.canvas.create_text(pos.x, pos.y, text=self.text, fill=self.color, font=(config.FONT, self.actualSize))
    def getSize():
        bounds = globals.canvas.canvas.bbox(self.text)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return Pos(width, height)
    def moveto(self, pos=None):
        if pos == None:
            pos = self.scale
        globals.canvas.canvas.moveto(self.obj, self.actual(self.scale).x, self.actual(self.scale).y)
    def update(self):
        print(self.actualSize, self.size, globals.canvas.screenSize.x)
        globals.canvas.canvas.itemconfig(self.obj, font=(config.FONT, self.actualSize))
        self.moveto()
        # globals.canvas.canvas.moveto(self.text, x + (width - textWidth) / 2, y + (height - textHeight) - 10)

# scale refers to relative position
class Button: # a button on tk canvas because yes
    def __init__(self, clickFunc, bg, text):
        self.bg = bg
        self.text = text
        self.click = clickFunc
        self.update()
        self.bindEvents()
    def moveTo(self, scale):
        pass
    def update(self):
        globals.canvas.canvas.coords(self.bg, self.bg.scale.x, self.bg.scale.y, self.bg.scale.x + self.bg.size.x, self.bg.scale.y + self.bg.size.y)
        self.text.update()
    def bindEvent(self, evt, func):
        globals.canvas.canvas.tag_bind(self.bg, evt, func)
        globals.canvas.canvas.tag_bind(self.text.obj, evt, func)
    def bindEvents(self):
        self.bindEvent("<Button-1>", self.click)
    def delete(self):
        globals.canvas.canvas.delete(self.bg)
        self.text.delete()

class Notification:
    def __init__(self, text):
        # self.background = globals.canvas.canvas.create_rectangle(0, 0, 0, 0, fill="grey", outline="white")
        self.background = Rect(globals.canvas.centerOf(bgDim), bgDim, fill="grey", outline="white")
        self.text = Text(fontSize, text)
        buttonPos = globals.canvas.centerOf(textDim, self.background.scale)
        buttonPos.y = self.background.scale.y + self.background.size.y
        self.button = Button(
            self.close,
            Rect(buttonPos, textDim, fill=draw.RED, activeFill=draw.DARKRED),
            Text(globals.canvas.centerOf(textDim, buttonPos), fontSize, "close")
        )
        globals.canvas.bindToResize(self.update)
        self.update()
    def close(self, e):
        self.delete()
    def update(self):
        self.background.update()
        self.text.update()
        self.button.update()
        # globals.canvas.canvas.coords(self.background, x, y, x + width, y + height)
        # globals.canvas.canvas.itemconfig(self.text, font=(config.FONT, int(w * fontSize)))
        # textWidth, textHeight = getTextDimensions(self.text)
        # globals.canvas.canvas.moveto(self.text, x + (width - textWidth) / 2, y + (height - textHeight) - 10)
        # globals.canvas.canvas.scale(self.background, 0, 0, (width * WIDTH), HEIGHT / height)
        # globals.canvas.canvas.moveto(self.background, x, y)
