import cProfile
import pygame
import random
import Game


# DISCLAIMER: INSPIRED BY https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/


def main():
    # Initialize pygame (for rendering text)
    pygame.init()

    # Create the Window of size (250x500)
    size = (250, 500)
    screen = pygame.display.set_mode(size)

    # Set Title of Window to 'Tetris'
    pygame.display.set_caption("Tetris")

    # Main Game initialization and Iteration

    screen_rect = (0, 0) + size
    # decent_coefficients = {"full_rows": 3, "bumpiness": -1, "dist_to_top": 3, "overhangs": -15, "percent_filled": 18}
    # weak_coefficients = {"full_rows": .4,  "bumpiness": 0, "dist_to_top": 2, "overhangs": -20, "percent_filled": 0}
    # bad_coefficients = {"full_rows": .2,  "bumpiness": -.2, "dist_to_top": 6, "overhangs": -2, "percent_filled": 3}
    very_solid = {'full_rows': 4.0097496350377515, 'bumpiness': -0.9153213934444262, 'dist_to_top':
        2.529587164513865, 'overhangs': -19.9046787649053, 'percent_filled': 21.79378411874574}
    # COEFFICIENTS: {'full_rows': 3.9477970286673854, 'bumpiness': -0.9071288880833255, 'dist_to_top': 2.4868517556555165, 'overhangs': -19.865389610599795, 'percent_filled': 22.06986273126868}

    print("BEGIN TEST")
    print()
    print()

    base_coefficients = very_solid
    game_instances = {}
    varied_outcomes = {}
    variation_num = 8  # number of variations to run
    repetition_per_variation = 1  # repeats of each individual variation

    for variation in range(variation_num):
        print("RUN " + str(variation + 1))

        # randomizing coefficients for different variations
        new_coefficients = {}
        for key in base_coefficients.keys():
            old_coefficient = base_coefficients.get(key, 0)
            new_coefficients[key] = old_coefficient + (random.random() - .5) * old_coefficient * 0.05

        # printing and storing variation
        print("COEFFICIENTS: " + str(new_coefficients))
        varied_outcomes[variation] = {"coefficients": new_coefficients, "scores": [], "average": None}

        for outcome in range(repetition_per_variation):
            final = True if (variation_num - 1) == variation and (outcome - 1) == repetition_per_variation else False
            instance_index = variation * variation_num + outcome

            # creating game instance
            game_instances[instance_index] = Game.Game(screen, screen_rect, new_coefficients, final)

            try:
                # run game...
                game_score = game_instances.get(instance_index).play()
            except Exception as e:
                # ... unless an un-handled error occurs
                print("Error:  ", str(e.args))
                game_score = 0

            # saving variations' scores
            varied_outcomes.get(variation).get("scores").append(game_score)
            print("FINAL SCORE: " + str(game_score))

        # and each given variations' average score
        average = sum(varied_outcomes.get(variation).get("scores")) / repetition_per_variation
        varied_outcomes[variation]["average"] = average
        print("AVERAGE: " + str(average))
        print()

    print("END TEST")

    print()
    print(varied_outcomes)


if __name__ == "__main__":
    # cProfile.run('main()', sort='cumulative')
    main()
    # Main Program
