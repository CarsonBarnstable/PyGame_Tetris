import pygame
import Piece
import Mass
import AuxiliaryIntelligence
from ScoreCalculations import get_score

import sys
import time


class Game:
    # Single instance of a Game

    def __init__(self, game_screen, screen_rect, in_coefficients, should_close=True):

        # Initialize Continuation Condition
        self.close_after_game = should_close

        # Initializes Game to be displayed
        self.do_ai = True
        self.draw_possibilities = False
        self.calculate_possibilities_scores = self.do_ai
        self.calculate_best_move = self.do_ai
        self.make_best_move = self.do_ai

        self.possibility_drawing_time_interval = 0.09
        self.computer_fall_speed = 10000
        self.coefficients = in_coefficients

        # Initialize Game Screen and Background Color
        self.screen = game_screen
        self.bg_color = pygame.Color("black")
        self.grid_color = pygame.Color("white")
        self.grid_thickness = 1

        # Initialize Game Clock
        self.game_clock = pygame.time.Clock()
        self.frames_per_second = 1200
        self.falling_speed = .1
        self.fall_speed_multiplier = 5

        # Initialize Game-Over conditions
        self.continue_game = True
        self.close_button_clicked = False

        # Initialize Game Attributes
        self.top_left_corner = screen_rect[:2]
        self.screen_size = screen_rect[2:]
        self.grid_size = (10, 20)
        self.score_points = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        self.tile_size = [self.screen_size[d]//self.grid_size[d] for d in range(len(self.grid_size))]

        # Initialize Score Variables
        self.score = 0
        self.increment_score_by_rows(0)
        self.score_font_size = self.screen_size[1]//10
        self.dp_antialias = True
        self.score_color = pygame.Color("white")
        self.score_bg_color = (0, 0, 0, 0)

        # Set Up Game
        self.active_piece = self.new_piece()
        self.mass = Mass.Mass(self.screen, self.grid_thickness)

        if self.do_ai:
            if not self.draw_possibilities:
                self.falling_speed = self.computer_fall_speed

    def play(self):
        # Play the game until the player presses the close box
        while self.continue_game and not self.close_button_clicked:
            if self.do_ai:
                # just do its own thing to place the blocks
                self.intelligence_test()
            self.handle_events(self.do_ai)

            # drawing
            self.draw()

            # IF gameplay should continue (end conditions are not met yet)
            if self.continue_game:
                self.update()
                self.decide_continue()

                if not self.continue_game:
                    break

            # Caps frame rate at (frames_per_second)
            self.game_clock.tick(self.frames_per_second)

        # Actually QUITs game once main loop is over (once close_button ic clicked)
        if self.close_after_game:
            game_quit()

        return self.score

    def handle_events(self, ai_active):
        # Event Handling (for all event types)
        # self - type: Game - role: Game's whose events will be handled

        for event in pygame.event.get():

            # Check for 'X' Button Being Pressed
            if event.type == pygame.QUIT:
                self.close_button_clicked = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.toggle_pause()

            if not ai_active and self.continue_game:
                # Check for Key Presses
                if event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.falling_speed = self.falling_speed / self.fall_speed_multiplier

    def draw(self):
        # Draws a new Background every Frame

        # Fills background w/ background color
        self.screen.fill(self.bg_color)

        # Draw Active Tile
        self.active_piece.draw()

        # Draw Mass
        self.mass.draw()

        # Draws Score
        self.draw_score()

        # Draws Tile Grid
        self.draw_tiles()

        # Draws (and renders) all objects to the screen
        pygame.display.flip()

    def draw_score(self):
        # Draws the Score in white on the window's background

        # Set up Printing Strings
        text_score = str(self.score)
        text_font = pygame.font.SysFont('Sans', self.score_font_size)

        # Create (and draw) the Left Player's Score
        score_image = text_font.render(text_score, self.dp_antialias, self.score_color, None)
        text_left_top_left_corner = (self.screen.get_width()-score_image.get_width(), 0)
        self.screen.blit(score_image, text_left_top_left_corner)

    def decide_continue(self):
        # Checks to see if game should continue
        self.continue_game = not self.mass.exists_above_top(self.top_left_corner[1])
        if not self.continue_game:
            self.increment_score_by_rows(0)

    def update(self):
        # Updates Game State
        self.active_piece.fall(self.falling_speed)
        if self.active_piece.touches_mass_or_bottom(self.mass.positions()):
            self.handle_piece_touching_mass()
        self.handle_full_rows()

    def handle_key_press(self, key):
        # Handles keys being pressed
        if key == pygame.K_LEFT:
            self.move_active_piece_horizontally('L')
        if key == pygame.K_RIGHT:
            self.move_active_piece_horizontally('R')
        if key == pygame.K_DOWN:
            self.falling_speed = self.falling_speed * self.fall_speed_multiplier
        if key == pygame.K_SPACE:
            self.active_piece.force_down_to(self.mass.positions())
        if key == pygame.K_z:
            self.rotate_active_piece("CCW")
        if key == pygame.K_x:
            self.rotate_active_piece("CW")

    # draws all tiles (to form grid)
    def draw_tiles(self):
        # Individually Draws all Tiles
        for x_pos in range(self.grid_size[0]):
            for y_pos in range(self.grid_size[1]):
                this_rect = [x_pos*self.tile_size[0], y_pos*self.tile_size[1]] + self.tile_size
                pygame.draw.rect(self.screen, self.grid_color, this_rect, self.grid_thickness)

    # instantiates new piece
    def new_piece(self):
        return Piece.Piece(self.screen, self.top_left_corner, self.grid_size, self.tile_size)

    # determines what happens when the "mass" gets touched
    def handle_piece_touching_mass(self):
        self.mass.add(self.active_piece.get_info())
        self.active_piece = self.new_piece()

    # moves falling piece either left or right (if allowed)
    def move_active_piece_horizontally(self, direction):
        # Moves piece Left/Right along Grid
        shift_direction = 0
        if direction == 'L':
            shift_direction = -1
        if direction == 'R':
            shift_direction = 1

        self.active_piece.shift(shift_direction * self.tile_size[0])

    # rotates falling piece either left or right (if allowed)
    def rotate_active_piece(self, rot_direction):
        shift_matrix = (0, 0)
        if rot_direction == "CCW":
            shift_matrix = (1, -1)
        if rot_direction == "CW":
            shift_matrix = (-1, 1)

        self.active_piece.rotate(shift_matrix)

        if self.active_piece.rotation_was_illegal(shift_matrix, self.mass.positions()):
            self.rotate_active_piece(rot_direction)

    # deals with any full rows (updates score and shifts mass)
    def handle_full_rows(self):
        number_of_full_rows = self.mass.deal_with_full_rows(self.grid_size, self.tile_size)
        if number_of_full_rows > 0:
            self.increment_score_by_rows(number_of_full_rows)
        if number_of_full_rows == -1:  # vertical overflow
            return

    # increments score according to score schema
    def increment_score_by_rows(self, new_row_clears):
        self.score = self.score + self.score_points[new_row_clears]

    # toggles the pause
    def toggle_pause(self):
        self.continue_game = not self.continue_game

    # returns all possible valid outcomes given the circumstances
    def get_all_possible_outcomes(self):
        piece = self.active_piece.get_rects()
        mass_pos = self.mass.positions()
        tlc = self.top_left_corner
        s_size = self.screen_size
        g_size = self.grid_size
        t_size = self.tile_size

        current_info = AuxiliaryIntelligence.AuxiliaryIntelligence(piece, mass_pos, tlc, s_size, g_size, t_size)

        possibilities = current_info.get_all_possibilities()
        return possibilities

    # gets score for each possible outcome
    def get_scores_for(self, possibilities, coefficients):
        scores = {}
        for key, mass in possibilities.items():
            scores[key] = get_score(mass, self.grid_size, self.tile_size, coefficients)
        return scores

    @staticmethod
    # determines optimal (valid) move
    def get_optimal_move(in_scores):
        default_move = (0, 1)

        top_score = in_scores.get(default_move, 0)
        best_moves = default_move

        for key, temp_score in in_scores.items():
            if temp_score > top_score:
                top_score = temp_score
                best_moves = key

        return best_moves

    # makes move according to optimal choice of moves
    def make_move(self, rotation_num, x_shift, drop=True):
        for __ in range(rotation_num):
            self.active_piece.rotate((1, -1))

        overflow_catcher = self.grid_size[0]
        while self.active_piece.get_centre_x() != x_shift and overflow_catcher:
            direction = 0
            if self.active_piece.get_centre_x() > x_shift:
                direction = -1
            if self.active_piece.get_centre_x() < x_shift:
                direction = 1
            self.active_piece.shift(direction * self.tile_size[0])

            overflow_catcher -= 1

        while drop and not self.active_piece.touches_mass_or_bottom(self.mass.positions()):
            self.draw()
            self.active_piece.fall(self.falling_speed * self.computer_fall_speed)

    # prints all possible possibilities before making it
    def print_all(self, possibilities):
        for key in possibilities.keys():

            self.screen.fill(self.bg_color)
            for rect in possibilities[key]:
                pygame.draw.rect(self.screen, self.score_color, rect)

            pygame.display.flip()
            time.sleep(self.possibility_drawing_time_interval)

    # conducts intelligence test
    def intelligence_test(self):
        coefficients = self.coefficients

        all_possibilities = self.get_all_possible_outcomes()
        all_scores = {}

        if self.draw_possibilities:
            self.print_all(all_possibilities)

        if self.calculate_possibilities_scores:
            all_scores = self.get_scores_for(all_possibilities, coefficients)

        if self.calculate_best_move and self.calculate_possibilities_scores:
            best_move = self.get_optimal_move(all_scores)

            if self.make_best_move:
                num_of_rotations, x_shift = best_move
                self.make_move(num_of_rotations, x_shift)


# a true quit (close window)
def game_quit():
    pygame.quit()
    sys.exit()
