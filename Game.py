from GameGrid import GameGrid
from GameTree import GameTree


class Game(object):
    player_one_score = 0
    player_two_score = 0
    PLAYER_ONE_COLOR = (0, 0, 255)
    PLAYER_TWO_COLOR = (255, 0, 0)
    current_turn = -1
    game_tree_depth = 0
    game_grid = None
    game_tree = None
    running = False
    game_over = False
    width = 0
    height = 0
    winner = 0

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
            self.width = width
            self.height = height

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
        return GameTree(self.game_grid, self.game_tree_depth, self.current_turn)

    def draw_current_state(self):
        self.game_grid.draw()

    def get_player_color(self, player_id):
        if player_id == 1:
            return self.PLAYER_ONE_COLOR
        else:
            return self.PLAYER_TWO_COLOR

    def make_a_move_based_on_game_tree(self):
        if self.game_tree is not None:
            for root in self.game_tree.adjacency_list:
                root.childrenGrids.clear()
            self.game_tree.adjacency_list.clear()
            self.game_grid.childrenGrids.clear()
            del self.game_tree.adjacency_list
            del self.game_tree
        self.game_tree = self.generate_game_tree()
        self.game_tree.make_move()
        self.game_grid = self.game_tree.current_grid_state
        self.current_turn = self.current_turn * -1
        self.update_score()

    def make_a_move_based_on_selected_line(self, line):
        box_won = self.game_grid.draw_line_and_win_box(line.array_index, self.current_turn)
        if not box_won:
            self.current_turn = self.current_turn * -1
        self.update_score()

    def update_score(self):
        self.player_one_score = self.game_grid.get_owned_boxes(1)
        self.player_two_score = self.game_grid.get_owned_boxes(-1)
        print("Total: " + str(self.player_one_score + self.player_two_score))
        print("Total box count:" + str(((self.width * (self.height - 2)) + 1)))
        if int(self.player_one_score + self.player_two_score) == int((self.width * (self.height - 2)) + 1):
            # game is over
            self.game_over = True

    def find_available_line_on_cursor_location(self, cursor_location):
        return self.game_grid.find_available_line_on_cursor_location(cursor_location)

    def current_player(self):
        if self.current_turn == -1:
            return "Player 2 Turn"
        else:
            return "Player 1 Turn"

    def display_winner(self):
        if int(self.player_one_score) > int(self.player_two_score):
            self.winner = 1
            return "Player One Wins"
        else:
            self.winner = -1
            return "Player Two Wins"
