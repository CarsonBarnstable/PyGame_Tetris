import pygame


class Mass:
    # Entire "Sitting Mass"

    def __init__(self, screen, grid_thickness):
        # Initializes the Entire Mass

        # Initialize Basic Visual Variables
        self.screen = screen

        # Setting up Mass
        self.pieces = []

        # and noting Border Thickness
        self.border_thickness = grid_thickness

    def draw(self):
        # Draws the Tile at its position, and a border around it (for grid spacing)

        # Draw Tile (then border) to screen
        for piece in self.pieces:
            piece_color, piece_rectangle = piece
            pygame.draw.rect(self.screen, piece_color, piece_rectangle)

    def positions(self):
        return self.pieces

    def exists_above_top(self, top):
        return any(piece[1][1] < top for piece in self.pieces)

    def add(self, new_piece):
        self.pieces += [(new_piece[0], chunk) for chunk in new_piece[1]]

    # TODO": re-isolate and fix
    def check_for_full_row(self, row_y_value, full_row_size, vertical_drop):
        if sum(piece[1][1] == row_y_value for piece in self.pieces) == full_row_size:
            for piece_index in range(len(self.pieces)-1, -1, -1):
                piece_y_index = self.pieces[piece_index][1][1]

                if piece_y_index == row_y_value:
                    self.pieces.remove(self.pieces[piece_index])
                elif piece_y_index < row_y_value:
                    self.pieces[piece_index][1][1] = piece_y_index + vertical_drop

            return 1
        # else
        return 0
