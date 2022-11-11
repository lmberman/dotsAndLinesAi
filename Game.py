from GameGrid import GameGrid
from GameTree import GameTree


class Game(object):
    player_one_score = 0
    player_two_score = 0
    PLAYER_ONE_COLOR = (0, 0, 255)
    PLAYER_TWO_COLOR = (255, 0, 0)
    current_turn = 1
    game_tree_depth = 0
    game_grid = None
    game_tree = None
    running = False

    # Initialize Game with 0 points for each player, a given size, and a given search depth
    def __init__(self, width, height, game_tree_depth):
        if width < 3 or height < 3:
            print("Unable to create game as grid is too small")
        else:
            self.player_one_score = 0
            self.player_two_score = 0
            self.game_tree_depth = game_tree_depth
            self.game_grid = GameGrid()
            self.game_grid.id = 1
            self.game_grid.with_dimensions(width, height)
            self.game_grid.create_empty_grid()
            self.game_tree = self.generate_game_tree()

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
        Use Game_Grid in order to generate the next states (future game_grids) of the current state by creating a
        list of game_grids each with the results of making a move and then setting it to the game
        """
        return GameTree(self.game_grid, self.game_tree_depth)

    def draw_current_state(self):
        self.game_grid.draw()

    def get_player_color(self, player_id):
        if player_id == 1:
            return self.PLAYER_ONE_COLOR
        else:
            return self.PLAYER_TWO_COLOR
