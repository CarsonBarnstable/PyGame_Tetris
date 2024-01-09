from Main import setup_game_instance, setup_pygame_window
from ScoreCalculations import normalize, variate

import multiprocessing
import time


def execute_run(coefficients=None, variance=0.0, repeats=1, use_threads=4, window_size=(250, 500)):
    # Base Case?
    if coefficients is None:
        coefficients = {param: 0 for param in ['full_rows', 'bumpiness', 'dist_to_top', 'overhangs', 'percent_filled']}

    # slightly randomize coefficients
    test_coefficients = [variate(coefficients, variance) for _ in range(repeats)]
    test_coefficients = [normalize(test_co) for test_co in test_coefficients]  # then normalizing

    # Running Requested Test
    inputs = [(use_coefficients, window_size) for use_coefficients in test_coefficients]
    with multiprocessing.Pool(use_threads) as p:
        pooled_scores = p.starmap(process_game, inputs)
    return pooled_scores, test_coefficients


def process_game(use_coefficients, window_size):
    screen, screen_canvas = setup_pygame_window(window_size)
    game_instance = setup_game_instance(screen, screen_canvas, use_coefficients, close_afterward=False)
    score = game_instance.play()
    return score


if __name__ == "__main__":
    test_values = {'full_rows': 0.0659733288908669,
                   'bumpiness': -0.018742896904640226,
                   'dist_to_top': 0.06519767646347654,
                   'overhangs': -0.33923109673040946,
                   'percent_filled': 0.5108550010106069
                   }
    test_var = 0.5
    repetitions = 20
    threads = 4

    # Main Program (Test Iteration)
    start_time = time.time()
    scores, used_coefficients = execute_run(test_values, variance=test_var, repeats=repetitions, use_threads=threads)
    test_output = sorted([(score, u_co) for score, u_co in zip(scores, used_coefficients)], key=lambda x: x[0])
    end_time = time.time()

    # and Printing Useful Output Details
    print("Data Output:", test_output)
    print("Scores:", sorted(scores))
    print("Total Test Time: ", end_time-start_time, "seconds")
