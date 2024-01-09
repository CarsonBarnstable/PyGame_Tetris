import pygame
import Game


# DISCLAIMER: INSPIRED BY https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/

def main(screen_size, use_coefficients):
    # setup
    screen, screen_canvas = setup_pygame_window(screen_size)
    game_instance = setup_game_instance(screen, screen_canvas, use_coefficients, close_afterward=False)

    # running
    try:
        # run game...
        game_score = game_instance.play()
    except Exception as e:
        # ... unless an un-handled error occurs
        print("Error:  ", str(e.args))
        game_score = 0
        raise e

    # useful return
    return game_score


def setup_pygame_window(window_size):
    # Initialize pygame (for rendering text)
    pygame.init()

    # Create the Window of size (250x500)
    size = window_size
    screen = pygame.display.set_mode(size)

    # Set Title of Window to 'Tetris'
    pygame.display.set_caption("PyGame Tetris")
    screen_rect = (0, 0) + window_size
    return screen, screen_rect


def setup_game_instance(screen, canvas, coefficients, close_afterward=True):
    return Game.Game(screen, canvas, coefficients, should_close=close_afterward)


if __name__ == "__main__":
    # test values
    test_screen_size = (250, 500)
    test_values = {'full_rows': 4.0097496350377515, 'bumpiness': -0.9153213934444262, 'dist_to_top': 2.529587164513865,
                   'overhangs': -19.9046787649053, 'percent_filled': 21.79378411874574}

    # run program
    score = main(test_screen_size, test_values)
    print("Test run Score:", score)
    # Main Program
