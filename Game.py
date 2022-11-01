import GameGrid
import GameTree


class Game:
    def __init__(self, width, length, player_one_score, player_two_score, game_tree_depth):
        if width < 3 or length < 3:
            print("Unable to create game as grid is too small")
        else:
            self.player_one_score = player_one_score
            self.player_two_score = player_two_score
            self.game_grid = GameGrid(width, length)
            self.game_tree = self.generate_game_tree()
            self.game_tree_depth = game_tree_depth

    def update_player_score(self, number, score):
        if number == 1:
            self.player_one_score = score
        else:
            self.player_two_score = score

    def update_grid_state(self, game_grid):
        self.game_grid = game_grid

    # generate layers of game tree from current game grid state down to the given depth since we will only need to
    # search down to this depth
    def generate_game_tree(self):
        """
        Use Game_Grid in order to generate the next states (future game_grids) of the current state by creating a list of game_grids each with the results of making a move
        and then setting it to the game
        """
        return GameTree(self.game_grid, self.game_tree_depth)




