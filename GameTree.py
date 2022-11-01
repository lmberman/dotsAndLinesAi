import GameGrid


class GameTree:
    def __init__(self, current_grid_state, depth):
        self.current_grid_state = current_grid_state
        self.future_grid_states = self.generate_future_states_to_depth(depth)

    def generate_future_states_to_depth(self, depth):
        current_game_grid = GameGrid(self.current_grid_state)
        for i in range(depth):
        # make all possible moves from the current game grid and set to children of currentGameGrid
            for line in current_game_grid.get_empty_lines:
                next_game_grid = GameGrid(current_game_grid)

        return 0

