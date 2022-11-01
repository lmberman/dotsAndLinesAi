"""
    This dict will maintain the structure of the dots and lines game grid
"""
import Dot
import Line


class GameGrid:
    def __init__(self, width, length):
        self.dots = []
        self.lines = []
        self.boxes = []
        self.parent
        self.children
        """
            lines (0,0 to 0,1), (0,0 to 1,0),
                  each dot gets a line between it and its predecessor in the same row, unless it is in the first column (0)
                  each dot gets a line between it and its upstairs neighbor, unless it is in the first row (0)
                  boxes are (0,0),(
        """
        for row in range(length):
            for column in range(width):
                # create dot
                dot = Dot(row, column)
                if row != 0:
                    """
                    connect upstairs neighbor
                    """
                    upstairs_dot = self.dots[len(self.dots) - width]
                    line = Line(dot, upstairs_dot)
                    # lines have a drawn attribute which is false by default so no
                    # need to set this when initializing the start gameGrid
                    self.lines.append(line)
                if column != 0:
                    """
                    connect predecessor in same row
                    """
                    predecessor = self.dots[len(self.dots) - 1]
                    line = Line(predecessor, dot)
                    self.lines.append(line)
                self.dots.append(dot)
                # need to figure out how to set the boxes and then set self.boxes. This will assist with evaluation

    def __init__(self, other_game_grid):
        self.dots = other_game_grid.dots
        self.lines = other_game_grid.lines
        self.boxes = other_game_grid.boxes

    def get_empty_lines(self):
        empty_lines = []
        for line in self.lines:
            if not line.drawn:
                empty_lines.append(line)
        return empty_lines
