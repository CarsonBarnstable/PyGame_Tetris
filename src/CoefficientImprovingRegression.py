from Main import setup_game_instance, setup_pygame_window
import random
import multiprocessing


def main(coefficients_start=None, variation_percent_start=100, test_repeats=1, iterations=-1, window_size=(250, 500)):
    # score = process_game(coefficients_start, variation_percent_start, test_repeats, iterations, window_size)
    
    inputs = [(coefficients_start, variation_percent_start, test_repeats, iterations, window_size) for _ in range(20)]
    with multiprocessing.Pool(4) as p:
        pooled_scores = p.starmap(process_game, inputs)
    print(pooled_scores)


def process_game(coefficients_start, variation_percent_start, test_repeats, iterations, window_size):
    screen, screen_canvas = setup_pygame_window(window_size)
    game_instance = setup_game_instance(screen, screen_canvas, coefficients_start, close_afterward=False)
    score = game_instance.play()
    return score


if __name__ == "__main__":
    start_values = {'full_rows': 4.0097496350377515, 'bumpiness': -0.9153213934444262, 'dist_to_top': 2.529587164513865,
                    'overhangs': -19.9046787649053, 'percent_filled': 21.79378411874574}
    # Main Program (Iteration Start)
    main(coefficients_start=start_values, variation_percent_start=50, test_repeats=20, iterations=0)
