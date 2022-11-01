class Line:

    def __init__(self):
        self.connectingDots = []
        self.drawn = False

    def set_connecting_dots(self, dot1, dot2):
        self.connectingDots = [dot1, dot2]

    def is_drawn(self):
        return self.drawn;
