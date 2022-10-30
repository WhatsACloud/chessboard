import config

class Pos(): # actual pos
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def __repr__(self):
        return str(self.x) + " " + str(self.y)
    def __sub__(self, other):
        other = self.isValid(other)
        return type(self)(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        other = self.isValid(other)
        return type(self)(self.x + other.x, self.y + other.y)
    def __truediv__(self, other):
        other = self.isValid(other)
        return type(self)(self.x / other.x, self.y / other.y)
    def __mul__(self, other):
        other = self.isValid(other)
        return type(self)(self.x * other.x, self.y * other.y)
    def __round__(self, ndigits=0):
        return type(self)(round(self.x, ndigits), round(self.y, ndigits))
    def __le__(self, other):
        other = self.isValid(other)
        return self.x <= other.x and self.y <= other.y
    def __ge__(self, other):
        other = self.isValid(other)
        return self.x >= other.x and self.y >= other.y
    def __eq__(self, other):
        return type(self) == type(other) and self.x == other.x and self.y == other.y
    def __deepcopy__(self, other):
        return type(self)(self.x, self.y)
    def __hash__(self):
        return hash((self.x, self.y))
    def inside(self, start, end):
        return start <= self <= end
    def isValid(self, other): # check if variable is of same class
        isPos = isinstance(other, type(self))
        isInt = isinstance(other, int)
        if not isPos and not isInt:
            raise TypeError(f"Second variable operating is not of class {type(self)} but is of type {type(other)}")
        if isInt:
            return type(self)(other, other)
        return other

class BoardPos(Pos): # board pos
    def exceedsBoard(self):
        more = self.x >= config.BOARD_LENGTH or self.y >= config.BOARD_LENGTH
        less = self.x < 0 or self.y < 0
        if more or less:
            return True
        return False
