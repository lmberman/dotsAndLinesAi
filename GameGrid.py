"""
    This dict will maintain the structure of the dots and lines game grid
"""
from Dot import Dot
from Line import Line
from Box import Box
from copy import deepcopy
import pygame


class GameGrid(object):
    id = 0
    dots = []
    lines = []
    boxes = []
    childrenGrids = []
    width = 0
    height = 0
    utility_value = 0

    def __init__(self):
        self.dots = []
        self.lines = []
        self.boxes = []
        self.childrenGrids = []
        self.id = 0
        self.utility_value = 0

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    # def __deepcopy__(self, memodict={}):
    #     self.width = other_game_grid.width
    #     self.height = other_game_grid.height
    #     self.dots = other_game_grid.dots
    #     self.lines = other_game_grid.lines
    #     self.boxes = other_game_grid.boxes
    #     return self

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

                if len(self.lines) > self.width + 1:
                    # need to distinguish the boxes to be created in the game
                    # pairing lines for boxes are any that end at the current dot or start
                    # at the dot with index row-1, column-1
                    self.find_boxes_lines(row, column)

                # need to figure out how to set the boxes and then set self.boxes. This will assist with evaluation
                # known information: We know all boxes are not owned by anyone at the time of initialization
                # and all lines of those boxes are not drawn at the time of initialization

    def find_boxes_lines(self, end_x, end_y):
        box = None
        new_box = False
        if len(self.boxes) == 0 or len(self.boxes[len(self.boxes)-1].lines) == 4:
            box = Box(len(self.boxes))
            box_lines = []
            new_box = True
        else:
            box = self.boxes[len(self.boxes) - 1]

        start_x = end_x
        start_y = end_y
        if start_x != 0:
            start_x = start_x - 1
        if start_y != 0:
            start_y = start_y - 1
        for line in self.lines:
            if line.starts_at(start_x, start_y) or line.ends_at(end_x, end_y):
                if len(line.box_ids) == 0:
                    box.lines.append(line)
                    line.add_box_id(box.box_id)
                else:
                    if not box.has_line(line.array_index):
                        line.add_box_id(box.box_id)
                        box.lines.append(line)
                # if line.box_id is not None:
                #     box = self.boxes[line.box_id-1]
                #     box_lines.append(line)
                # else:
                # check if box line isnt assigned to a box or it is shared between a neighboring box
                # (-1 for left neighbor and -3 for upstairs neighbor)

        if box is not None and new_box:
            self.boxes.append(box)

    def draw_line_and_win_box(self, line_index, owner):
        line = self.lines[line_index]
        line.mark_as_drawn(owner)
        completed_a_box = False
        for box_id in line.box_ids:
            self.boxes[box_id].update_line(line)
            completed_box = self.boxes[box_id].is_complete()
            if completed_box:
                self.boxes[box_id].set_owner(owner)
                if not completed_a_box:
                    completed_a_box = True
        return completed_a_box

    """
        Evaluate the utility value of this grid (node) to determine how likely it is for the current player to win
        rules are:
            -1 points for box with three lines
            0 points for boxes with one line
            1 point for boxes with two lines
            2 points for box owned by player, -2 points for boxes not owned by player
            2 * number of boxes owned by player, -2 * number of boxes not owned by player
    """

    def evaluate_winning_stats(self, player):
        for box in self.boxes:
            line_count = box.num_of_drawn_lines()
            if line_count == 1:
                """ do nothing since zero points are given for this move """
                self.utility_value = (self.utility_value + 1) * player
            if line_count == 2:
                self.utility_value = (self.utility_value + 2) * player
            if line_count == 3:
                self.utility_value = (self.utility_value - 3) * player
            if line_count == 4 and box.owner == player:
                self.utility_value = 4 * player
        return self.utility_value

    def get_owned_boxes(self, owner):
        num_of_boxes = 0
        for box in self.boxes:
            if box.owner == owner:
                num_of_boxes = num_of_boxes + 1
        return num_of_boxes

    def find_available_line_on_cursor_location(self, cursor_location):
        available_lines = self.get_empty_lines()
        for line in available_lines:
            if line.surrounds(cursor_location):
                return line
