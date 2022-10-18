class Pos(): # actual pos
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def __repr__(self):
        return str(self.x) + " " + str(self.y)
    def __sub__(self, other):
        other = self.isValid(other)
        return Pos(self.x - other.x, self.y - other.y)
    def __add__(self, other):
        other = self.isValid(other)
        return Pos(self.x + other.x, self.y + other.y)
    def __truediv__(self, other):
        other = self.isValid(other)
        return Pos(self.x / other.x, self.y / other.y)
    def __mul__(self, other):
        other = self.isValid(other)
        return Pos(self.x * other.x, self.y * other.y)
    def __round__(self, ndigits=0):
        other = return Pos(round(self.x, ndigits), round(self.y, ndigits))
    def __le__(self, other):
        other = self.isValid(other)
        return self.x <= other.x and self.y <= other.y
    def __ge__(self, other):
        other = self.isValid(other)
        return self.x >= other.x and self.y >= other.y
    def __deepcopy__(self, other):
        return Pos(self.x, self.y)
    def inside(self, start, end):
        return start <= self <= end
    def isValid(self, other): # check if variable is of same class
        isPos = isinstance(other, Pos)
        isInt = isinstance(other, int)
        if not isPos and not isInt:
            raise TypeError(f"Second variable operating is not of class {type(self)} but is of type {type(other)}")
        if isInt:
            return Pos(other, other)
        return other

class BoardPos(Pos): # board pos
    pass
