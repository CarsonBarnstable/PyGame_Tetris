from Main import setup_game_instance, setup_pygame_window
from ScoreCalculations import normalize, variate

import multiprocessing
import time

# Which programs to Run
RUN_TEST_OUT = False
GENETIC_ALGO = True

# Controlling Genetic Algorithm
GENETIC_GENERATIONS = 6
GENETIC_ITERATIONS = 20  # per generation
CONCURRENT_GAMES = 4  # within generation
SURVIVAL_PROP = 0.3  # after each generation

# Controlling Genetic Iterations
GENERATION_VARIANCES = [0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
STARTING_PARAMS = {'full_rows': 0.0659733288908669,
                   'bumpiness': -0.018742896904640226,
                   'dist_to_top': 0.06519767646347654,
                   'overhangs': -0.33923109673040946,
                   'percent_filled': 0.5108550010106069
                   }

# Quick Parameter Checking
assert CONCURRENT_GAMES <= multiprocessing.cpu_count()  # terrible performance otherwise
assert len(GENERATION_VARIANCES) >= GENETIC_GENERATIONS  # ensuring there are adequate variances
assert all(VAR >= 0 for VAR in GENERATION_VARIANCES)  # just for logical randomized varying
assert 0 < SURVIVAL_PROP < 1


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


def print_params_per_score(result_scores, used_params, score_width=7, col_width=15, spacer=2, sort=True):
    all_params = ['full_rows', 'bumpiness', 'dist_to_top', 'overhangs', 'percent_filled']

    # sorting if necessary
    if sort:
        sorting_array = [(sc, par) for sc, par in zip(result_scores, used_params)]
        sorting_array.sort(key=lambda x: x[0])  # sort by score
        result_scores, used_params = list(zip(*sorting_array))

    # Printing Header Row
    print(" "*score_width, end=" "*spacer)
    for param in all_params:
        print(param[:col_width].center(col_width), end=" "*spacer)
    print()

    # printing all proceeding rows
    for score, score_params in zip(result_scores, used_params):
        print(str(score).rjust(score_width), end="")  # score
        print(" "*2, end="")  # break
        for param in score_params.values():
            print(str(param)[:col_width].ljust(col_width), end=" "*spacer)
        print()  # newline char


def print_run_details(data_out, scores, total_time, threads, repeats, coefficients):
    print("Data Output:", data_out)
    print("Scores:", sorted(scores))
    print("Total Test Time: ", total_time, "seconds")
    print("Average of", total_time/repeats, "seconds per game (", threads, "threads | ", repeats, "games )")
    print()
    print_params_per_score(scores, coefficients)


def do_test(print_output_timings=False):
    # Just fair values to show full performance of multithreaded program
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
    total_time = end_time-start_time

    # and Printing Useful Output Details
    if print_output_timings:
        print_run_details(test_output, scores, total_time, threads, repetitions, used_coefficients)


def do_genetic_algo(print_dialogue=False, print_best_parameters=True):
    generation_parameters = STARTING_PARAMS
    for generation in range(GENETIC_GENERATIONS):
        start_time = time.time()

        # Running Execution with Current Generation's Parameters
        scores, coefficients = execute_run(generation_parameters, variance=GENERATION_VARIANCES[generation],
                                           repeats=GENETIC_ITERATIONS, use_threads=CONCURRENT_GAMES)

        # Isolating Top Proportion of Runs
        score_coefficient = sorted([(score, co) for score, co in zip(scores, coefficients)], key=lambda x: x[0])
        top_half_score_coefficients = score_coefficient[int(GENETIC_ITERATIONS*(1-SURVIVAL_PROP)):]

        # Averaging Coefficients from Top Proportion
        for coefficient in STARTING_PARAMS.keys():
            generation_parameters[coefficient] = sum(attempt[1][coefficient] for attempt in top_half_score_coefficients)
        generation_parameters = normalize(generation_parameters)
        tot_time = time.time() - start_time

        # Printing (when Required)
        if print_dialogue:
            print()
            print("* "*5 + "GENERATION " + str(generation+1) + " *"*5)
            print()
            print_run_details(score_coefficient, scores, tot_time, CONCURRENT_GAMES, GENETIC_ITERATIONS, coefficients)
        if print_best_parameters:
            print("Generation: ", generation+1, ": ", generation_parameters)
            print()


if __name__ == "__main__":
    if RUN_TEST_OUT:
        do_test(print_output_timings=True)
    if GENETIC_ALGO:
        do_genetic_algo(print_dialogue=True)
