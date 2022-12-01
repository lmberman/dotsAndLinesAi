from GameGrid import GameGrid
from copy import deepcopy


class GameTree:
    # Two dimen array made up of all gameGrid(states) down to the configured depth
    adjacency_list = []

    def __init__(self, current_grid_state, depth, player):
        current_grid_state.childrenGrids.clear()
        self.current_grid_state = deepcopy(current_grid_state)
        self.adjacency_list = []
        self.generate_future_states_to_depth(current_grid_state, depth, player)
        self.current_grid_state = self.adjacency_list[0]

    # TODO: Need fully generated gameTree down to depth
    def generate_future_states_to_depth(self, grid, depth, owner):
        # make a new record in adj list if not in adjacency_list
        print("At depth " + str(depth) + " with grid id " + str(grid.id) + " and owner " + str(owner))
        if depth == 0:
            # grid.evaluate_winning_stats()
            return
        if len(self.adjacency_list) == 0:
            self.adjacency_list.append(grid)

        # create next layer below root or current grid
        self.create_children_of_grid(grid, owner)
        if len(grid.childrenGrids) > 0:
            print("Adjacency List Size After Children: " + str(len(self.adjacency_list)))
            index = 1
            for child in grid.childrenGrids:
                print(str(index) + ": Moving to the level to create " + str(len(grid.childrenGrids) - (index - 1))
                      + "children of grid id: " + str(grid.id))
                self.generate_future_states_to_depth(child, depth - 1, owner * -1)
                index = index + 1

    def is_in_adjacency_list(self, grid):
        if len(self.adjacency_list) < grid.id:
            return False
        else:
            return True

    def create_children_of_grid(self, grid, owner):
        children = []
        child_grid = None
        retry_again = False
        for line in grid.get_empty_lines():
            if not retry_again:
                print("Creating a new child to check if we can win")
                child_grid = deepcopy(grid)
                child_grid.id = len(self.adjacency_list)+1
            print("Checking if box won on line: " + str(line.array_index))
            box_won = child_grid.draw_line_and_win_box(line.array_index, owner)
            if box_won:
                retry_again = True
            else:
                retry_again = False
            children.append(child_grid)
            self.adjacency_list.append(child_grid)
        grid.childrenGrids = children

    """
        Determine the next move for the player to make based on the utility values at each node and alpha beta pruning
    """

    def find_next_move(self, start_node, alpha, beta, player):
        if start_node is None or start_node.id == 0:
            # take the current_grid_state to start which is always the root of the tree
            start_node = self.adjacency_list[0]
        else:
            if len(self.adjacency_list) == 0:
                return start_node.utility_value * player
            # get the node from the adjacency list, so we can grab its children
            print("Start Node Id in find Next Move: " + str(start_node.id) + " and adjacency list size:" + str(
                len(self.adjacency_list)))
            start_node = self.adjacency_list[start_node.id - 1]

        if len(start_node.childrenGrids) == 0:
            # terminal node
            return start_node.utility_value * player

        value = 1000 * player
        for child in start_node.childrenGrids:
            value = max(value, self.find_next_move(child, -beta, -alpha, -player))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def make_move(self):
        move_value = self.find_next_move(self.adjacency_list[0], 1000, -1000, 1)
        max_value = move_value
        next_move = None
        for node in self.adjacency_list[0].childrenGrids:
            if node.utility_value >= max_value:
                max_value = node.utility_value
                next_move = node
        if next_move is None:
            next_move = self.adjacency_list[0].childrenGrids[0]
        self.current_grid_state = self.adjacency_list[next_move.id-1]
        self.current_grid_state.id = 1

