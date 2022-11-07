from Dot import Dot


class Line:
    box_id = -1
    array_index = -1
    LINE_LENGTH = 100
    LINE_WIDTH = 4
    owner = 0

    def __init__(self, dot1, dot2, array_index):
        self.connectingDots = [dot1, dot2]
        self.drawn = False
        self.array_index = array_index

    def mark_as_drawn(self, owner):
        self.drawn = True
        self.owner = owner

    def starts_at(self, x, y):
        start_dot = self.connectingDots[0]
        return start_dot.indexX == x and start_dot.indexY == y

    def ends_at(self, x, y):
        end_dot = self.connectingDots[1]
        return end_dot.indexX == x and end_dot.indexY == y

    def set_box_id(self, box_id):
        self.box_id = box_id
