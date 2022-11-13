from Dot import Dot


class Line:
    box_ids = None
    array_index = -1
    LINE_LENGTH = 100
    LINE_WIDTH = 4
    owner = 0

    def __init__(self, dot1, dot2, array_index):
        self.connectingDots = [dot1, dot2]
        self.drawn = False
        self.array_index = array_index
        self.box_ids = []

    def mark_as_drawn(self, owner):
        self.drawn = True
        self.owner = owner

    def starts_at(self, x, y):
        start_dot = self.connectingDots[0]
        return start_dot.indexX == x and start_dot.indexY == y

    def ends_at(self, x, y):
        end_dot = self.connectingDots[1]
        return end_dot.indexX == x and end_dot.indexY == y

    def add_box_id(self, box_id):
        self.box_ids.append(box_id)

    def surrounds(self, cursor_location):
        line_start = self.connectingDots[0]
        line_end = self.connectingDots[1]
        mouse_x = cursor_location.__getitem__(0)
        mouse_y = cursor_location.__getitem__(1)
        horizontal_width_min = line_start.locationY - self.LINE_WIDTH
        horizontal_width_max = line_start.locationY + self.LINE_WIDTH
        vertical_width_min = line_start.locationX - self.LINE_WIDTH
        vertical_width_max = line_start.locationX + self.LINE_WIDTH

        # print("Comparing line: (" + str(line_start.locationX) + "," + str(line_start.locationY) + ") to ( "
        #       + str(line_end.locationX) + "," + str(line_end.locationY)
        #       + ") with mouse_location: (" + str(mouse_x) + "," + str(mouse_y) + ") "
        #       + "horizontal Y limits: " + str(horizontal_width_min) + "," + str(horizontal_width_max)
        #       + " and vertical X limits: " + str(vertical_width_min) + "," + str(vertical_width_max))
        if ((line_start.locationX < mouse_x < line_end.locationX and
             horizontal_width_min <= mouse_y <= horizontal_width_max) or
                (vertical_width_min <= mouse_x <= vertical_width_max
                 and line_start.locationY < mouse_y < line_end.locationY)):
            # print("Match found " + str(line_start.locationX) + "," + str(line_start.locationY) + ") to ( "
            #       + str(line_end.locationX) + "," + str(line_end.locationY))
            return True

        return False
