from GameGrid import GameGrid
from copy import deepcopy


class GameTree:
    # Two dimen array made up of all gameGrid(states) down to the configured depth
    adjacency_list = []

    def __init__(self, current_grid_state, depth):
        self.current_grid_state = current_grid_state
        self.generate_future_states_to_depth(current_grid_state, depth, 1)

    # TODO: Need fully generated gameTree down to depth
    def generate_future_states_to_depth(self, grid, depth, owner):
        # make a new record in adj list if not in adjacency_list
        print("At depth " + str(depth) + " with grid id " + str(grid.id) + " and owner " + str(owner))
        if depth == 1:
            return
        if len(self.adjacency_list) == 0:
            self.adjacency_list.append(grid)

        self.create_children_of_grid(grid, owner)
        self.adjacency_list[grid.id - 1] = grid
        index = 1
        for child in grid.childrenGrids:
            print(str(index) + ": Creating the next level children for " + str(len(grid.childrenGrids)-(index-1))
                  + " of grid id: " + str(grid.id))
            self.generate_future_states_to_depth(child, depth - 1, owner * -1)
            index = index+1
        self.current_grid_state = self.adjacency_list[0]

    def is_in_adjacency_list(self, grid):
        if len(self.adjacency_list) < grid.id:
            return False
        else:
            return True

    def create_children_of_grid(self, grid, owner):
        children = []
        for line in grid.get_empty_lines():
            child_grid = deepcopy(grid)
            child_grid.id = len(self.adjacency_list)+1
            child_grid.draw_line_and_win_box(line.array_index, owner)
            children.append(child_grid)
            self.adjacency_list.append(child_grid)
        grid.childrenGrids = children
