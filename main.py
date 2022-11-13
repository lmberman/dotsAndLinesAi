from Game import Game
import selenium
import pygame
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dots and Lines")
BACKGROUND_COLOR = (255, 255, 255)
HEADER_COLOR = (0, 0, 0)
# Frames per second
FPS = 60
BOLD_FONT_FILE = 'freesansbold.ttf'
HEADER_FONT = pygame.font.Font(BOLD_FONT_FILE, 32)
STATS_FONT = pygame.font.Font(BOLD_FONT_FILE, 18)
GAME_OVER_FONT = pygame.font.Font(BOLD_FONT_FILE, 60)
BOARD_WIDTH, BOARD_HEIGHT = 4, 4
GAME_SEARCH_DEPTH = 2
LINE_LENGTH, LINE_WIDTH = 30, 3
GAME = Game(BOARD_WIDTH, BOARD_HEIGHT, GAME_SEARCH_DEPTH)


def draw_window():
    WIN.fill(BACKGROUND_COLOR)
    # display header
    text = HEADER_FONT.render("Dots and Boxes", False, HEADER_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 8)
    WIN.blit(text, text_rect)

    # player stats
    player_one = STATS_FONT.render("Player 1: " + str(GAME.player_one_score), False, GAME.PLAYER_ONE_COLOR)
    player_two = STATS_FONT.render("Player 2: " + str(GAME.player_two_score), False, GAME.PLAYER_TWO_COLOR)
    player_one_rect = player_one.get_rect()
    player_two_rect = player_two.get_rect()

    player_one_rect.center = (text_rect.centerx - 180, HEIGHT / 4)
    WIN.blit(player_one, player_one_rect)
    player_two_rect.center = (text_rect.centerx + 180, HEIGHT / 4)
    WIN.blit(player_two, player_two_rect)

    # whose turn is it?
    current_turn = STATS_FONT.render(GAME.current_player(), False, GAME.get_player_color(GAME.current_turn))
    current_turn_rect = current_turn.get_rect()

    current_turn_rect.center = (text_rect.centerx, HEIGHT / 6)
    WIN.blit(current_turn, current_turn_rect)

    # display results
    for line in GAME.game_grid.lines:
        if line.drawn:
            pygame.draw.line(WIN,
                             GAME.get_player_color(int(line.owner)),
                             (line.connectingDots[0].locationX, line.connectingDots[0].locationY),
                             (line.connectingDots[1].locationX, line.connectingDots[1].locationY),
                             line.LINE_WIDTH)
    for dot in GAME.game_grid.dots:
        pygame.draw.circle(WIN, HEADER_COLOR, [dot.locationX, dot.locationY], 8)
    if GAME.game_over:
        # winner
        game_over = GAME_OVER_FONT.render(GAME.display_winner(), False, GAME.get_player_color(GAME.winner))
        game_over_rect = game_over.get_rect()

        game_over_rect.center = (text_rect.centerx, HEIGHT / 2)
        WIN.blit(game_over, game_over_rect)
    pygame.display.update()


def draw_line_for_player():
    mouse_location = pygame.mouse.get_pos()
    mouse_x = mouse_location.__getitem__(0)
    mouse_y = mouse_location.__getitem__(1)
    if mouse_x > 0 and mouse_y > 0:
        # print("Current mouse location on screen: " + str(mouse_x) + "," + str(mouse_y))
        line = GAME.find_available_line_on_cursor_location(mouse_location)
        if line is not None:
            GAME.make_a_move_based_on_selected_line(line)
    pygame.display.update()


def play_game():
    # second player moves first get position of mouse and determine if it is within the game screen limits and within
    # the domain of any available lines to draw
    if GAME.current_turn == -1:
        mouse_location = pygame.mouse.get_pos()
        mouse_x = mouse_location.__getitem__(0)
        mouse_y = mouse_location.__getitem__(1)
        if mouse_x > 0 and mouse_y > 0:
            # print("Current mouse location on screen: " + str(mouse_x) + "," + str(mouse_y))
            line = GAME.find_available_line_on_cursor_location(mouse_location)
            if line is not None:
                # print("Match found " + str(line.connectingDots[0].locationX) + "," + str(
                #     line.connectingDots[0].locationY) + ") to ( "
                #       + str(line.connectingDots[1].locationX) + "," + str(line.connectingDots[1].locationY))
                pygame.draw.line(WIN,
                                 GAME.get_player_color(int(GAME.current_turn)),
                                 (line.connectingDots[0].locationX, line.connectingDots[0].locationY),
                                 (line.connectingDots[1].locationX, line.connectingDots[1].locationY),
                                 line.LINE_WIDTH)
                pygame.display.update()
    else:
        # play next move for player
        GAME.make_a_move_based_on_game_tree()


def main():
    clock = pygame.time.Clock()
    GAME.running = True
    while GAME.running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # user quit the window
                GAME.running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and GAME.current_turn == -1:
                draw_line_for_player()
            draw_window()
            play_game()

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Initializing Game

    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
