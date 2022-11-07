from GameGrid import GameGrid


class GameTree:

    def __init__(self, current_grid_state, depth):
        self.current_grid_state = current_grid_state
        self.generate_future_states_to_depth(None, depth, 1)

    # TODO: Need fully generated gameTree down to depth
    def generate_future_states_to_depth(self, grid, depth, owner):
        if depth == 0:
            return grid.childrenGrids
        if grid is None:
            grid = self.current_grid_state
        # for all available_lines the player can draw make a new state in the game_tree and make the current
        # grid the new states parent so we can search the tree later using DFS.
        for line in grid.get_empty_lines():
            next_state = GameGrid()
            next_state.__copy__(grid)
            next_state.parentGrid = grid
            grid.childrenGrids.append(next_state)
            # while the next_state has empty lines and the player wins a box on each draw continue to draw the lines
            # while next_state.draw_line_and_win_box(line.array_index, owner):
            #     line = next_state.get_empty_lines[0]

            # children_states = self.generate_future_states_to_depth(next_state, depth-1, owner*-1)
            # next_state.childrenGrids.append(children_states)
        # self.current_grid_state = grid
