"""
    This dict will maintain the structure of the dots and lines game grid
"""
from Dot import Dot
from Line import Line
from Box import Box
import pygame


class GameGrid(object):
    dots = []
    lines = []
    boxes = []
    parentGrid = None
    childrenGrids = []
    line_width = 10
    width = 0
    height = 0

    def __init__(self):
        self.dots = []
        self.lines = []
        self.boxes = []
        self.parentGrid = None
        self.childrenGrids = []

    def __copy__(self, other_game_grid):
        self.width = other_game_grid.width
        self.height = other_game_grid.height
        self.dots = other_game_grid.dots
        self.lines = other_game_grid.lines
        self.boxes = other_game_grid.boxes
        return self

    def with_dimensions(self, width, height):
        self.width = width
        self.height = height


    def get_empty_lines(self):
        empty_lines = []
        for line in self.lines:
            if not line.drawn:
                empty_lines.append(line)
        return empty_lines

    def create_empty_grid(self):
        """
          lines (0,0 to 0,1), (0,0 to 1,0),
          each dot gets a line between it and its predecessor in the same row, unless it is in the first column (0)
          each dot gets a line between it and its upstairs neighbor, unless it is in the first row (0)
          boxes are (0,0),(
        """
        starting_x = 250
        starting_y = 200
        for row in range(self.height):
            if row != 0:
                starting_y = starting_y + Line.LINE_LENGTH
                starting_x = 250
            for column in range(self.width):
                # create dot
                dot = Dot(row, column)

                if row != 0:
                    """
                    connect upstairs neighbor
                    """
                    upstairs_dot = self.dots[len(self.dots) - self.width]
                    line = Line(upstairs_dot, dot, len(self.lines))
                    # lines have a drawn attribute which is false by default so no
                    # need to set this when initializing the start gameGrid
                    self.lines.append(line)
                if column != 0:
                    starting_x = starting_x + Line.LINE_LENGTH
                    """
                    connect predecessor in same row
                    """
                    predecessor = self.dots[len(self.dots) - 1]
                    line = Line(predecessor, dot, len(self.lines))
                    self.lines.append(line)
                dot.set_location(starting_x, starting_y)
                self.dots.append(dot)

                if len(self.lines) >= self.width + 1:
                    # need to distinguish the boxes to be created in the game
                    # pairing lines for boxes are any that end at the current dot or start
                    # at the dot with index row-1, column-1
                    self.find_boxes_lines(row, column)

                # need to figure out how to set the boxes and then set self.boxes. This will assist with evaluation
                # known information: We know all boxes are not owned by anyone at the time of initialization
                # and all lines of those boxes are not drawn at the time of initialization
    def find_boxes_lines(self, end_x, end_y):
        box = Box(len(self.boxes))
        box_lines = []
        start_x = end_x
        start_y = end_y
        if start_x != 0:
            start_x = start_x - 1
        if start_y != 0:
            start_y = start_y - 1
        for line in self.lines:
            if line.starts_at(start_x, start_y) or line.ends_at(end_x, end_y):
                line.set_box_id(box.box_id)
                box_lines.append(line)
        box.set_lines(box_lines)
        self.boxes.append(box)

    def draw_line_and_win_box(self, line_index, owner):
        line = self.lines[line_index]
        line.mark_as_drawn(owner)
        self.boxes[line.box_id].update_line(line)
        return self.boxes[line.box_id].is_complete()

