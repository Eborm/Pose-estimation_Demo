class ColorBGR:
    def __init__(self, b, g, r):
        self.b = b
        self.g = g
        self.r = r

    def to_tuple(self):
        return (self.b, self.g, self.r)