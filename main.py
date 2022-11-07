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
BOARD_WIDTH, BOARD_HEIGHT = 4, 4
GAME_SEARCH_DEPTH = 3
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

    for line in GAME.game_grid.lines:
        if line.drawn:
            pygame.draw.line(WIN,
                             GAME.get_player_color(int(line.owner)),
                             (line.connectingDots[0].locationX, line.connectingDots[0].locationY),
                             (line.connectingDots[1].locationX, line.connectingDots[1].locationY),
                             line.LINE_WIDTH)
    for dot in GAME.game_grid.dots:
        pygame.draw.circle(WIN, HEADER_COLOR, [dot.locationX, dot.locationY], 8)

    # TODO: Need to be able to draw a line on the page
    # TODO: Once line is chosen, mark it as drawn by user
    # TODO: If box is completed by move then increase the score (if have time color the box)
    # TODO: On player one's turn need to use GameTree and Evaluation function to determine next move
    # TODO: Make move for player one
    pygame.display.update()


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
            draw_window()

    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Initializing Game

    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
