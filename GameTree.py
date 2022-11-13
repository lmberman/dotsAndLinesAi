from GameGrid import GameGrid
from copy import deepcopy


class GameTree:
    # Two dimen array made up of all gameGrid(states) down to the configured depth
    adjacency_list = []

    def __init__(self, current_grid_state, depth, player):
        self.current_grid_state = deepcopy(current_grid_state)
        self.adjacency_list = []
        self.generate_future_states_to_depth(current_grid_state, depth, player)

    # TODO: Need fully generated gameTree down to depth
    def generate_future_states_to_depth(self, grid, depth, owner):
        # make a new record in adj list if not in adjacency_list
        print("At depth " + str(depth) + " with grid id " + str(grid.id) + " and owner " + str(owner))
        if depth == 1:
            # grid.evaluate_winning_stats()
            return
        if len(self.adjacency_list) == 0:
            self.adjacency_list.append(grid)

        self.create_children_of_grid(grid, owner)
        if len(grid.childrenGrids) > 0:
            print("Adjacency List Size After Children: " + str(len(self.adjacency_list)))
            self.adjacency_list[grid.id - 1] = grid
            index = 1
            for child in grid.childrenGrids:
                print(str(index) + ": Moving to the level to create " + str(len(grid.childrenGrids) - (index - 1))
                      + "children of grid id: " + str(grid.id))
                self.generate_future_states_to_depth(child, depth - 1, owner * -1)
                index = index + 1
            self.current_grid_state = self.adjacency_list[0]

    def is_in_adjacency_list(self, grid):
        if len(self.adjacency_list) < grid.id:
            return False
        else:
            return True

    def create_children_of_grid(self, grid, owner):
        print("Creating a new children for grid " + str(grid.id))
        children = []
        box_won = False
        child_grid = None
        for line in grid.get_empty_lines():
            if not box_won:
                print("Creating a new child to check if we can win")
                child_grid = deepcopy(grid)
                child_grid.id = len(self.adjacency_list) + 1
            print("Checking if box won on line: " + str(line.array_index))
            box_won = child_grid.draw_line_and_win_box(line.array_index, owner)
            if not box_won:
                print("Box not won by line: " + str(line.array_index))
                children.append(child_grid)
                if len(self.adjacency_list) > child_grid.id:
                    self.adjacency_list[child_grid.id - 1] = child_grid
                else:
                    self.adjacency_list.append(child_grid)
        grid.childrenGrids = children

    """
        Determine the next move for the player to make based on the utility values at each node and alpha beta pruning
    """

    def find_next_move(self, start_node, alpha, beta, player):
        if start_node is None:
            # take the current_grid_state to start which is always the root of the tree
            start_node = self.adjacency_list[0]
        else:
            if len(self.adjacency_list) == 0:
                return start_node.evaluate_winning_stats()
            # get the node from the adjacency list, so we can grab its children
            start_node = self.adjacency_list[start_node.id - 1]

        if len(start_node.childrenGrids) == 0:
            return start_node.evaluate_winning_stats()

        value = 1000
        for child in start_node.childrenGrids:
            value_of_next_move = self.find_next_move(child, -alpha, -beta, -player)
            value = max(value, value_of_next_move)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        start_node.utility_value = value
        return value

    def make_move(self):
        self.find_next_move(self.adjacency_list[0], 0, 0, 1)
        if self.adjacency_list[0].utility_value == 0:
            self.current_grid_state = self.adjacency_list[0].childrenGrids[0]
            return
        else:
            for child in self.adjacency_list[0].childrenGrids:
                if child.utility_value == self.adjacency_list[0].utility_value:
                    self.current_grid_state = self.adjacency_list[child.id - 1]
                    break
