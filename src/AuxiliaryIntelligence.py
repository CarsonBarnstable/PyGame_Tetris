import pygame


class AuxiliaryIntelligence:
    # Single instance of a Tile

    def __init__(self, piece, mass, tlc, screen_size, grid_size, tile_size):
        # Main Pieces
        self.initial_piece_rects = [pygame.Rect(rect) for rect in piece]
        self.initial_mass = [rect_info[1] for rect_info in mass]

        # Main Dimensions
        self.top_left_corner = tlc
        self.screen_size = screen_size
        self.grid_size = grid_size
        self.tile_size = tile_size

        # Major Dict
        self.valid_masses = {}

    def get_all_possibilities(self):
        self.center_piece()
        for __ in range(3):
            self.rotate_piece()

        # iterating through all possible starting rotations
        for rotation_iteration in range(4):
            self.rotate_piece()

            # iterating through all possible starting horizontal positions
            for x_coord in range(self.grid_size[0]):
                # assembling newly chosen piece
                pieces = [piece.move(x_coord * self.tile_size[0], 0) for piece in self.initial_piece_rects]

                if self.touches_sides(pieces):
                    continue

                self.drop_piece(pieces)
                for piece in pieces:
                    piece.move_ip(0, -1*self.tile_size[1])

                # taking notes of valid new configurations
                self.valid_masses[rotation_iteration, x_coord] = self.initial_mass + pieces

        return self.valid_masses

    def center_piece(self):
        prior_center = self.initial_piece_rects[0].topleft
        for rect in self.initial_piece_rects:
            rect.move_ip(-1*prior_center[0], -1*prior_center[1])

    def rotate_piece(self):
        # rotates a piece around it's pre-determined top-left corner
        centre_point = self.initial_piece_rects[0].topleft
        core_coords = [c_p/t_s for c_p, t_s in zip(centre_point, self.tile_size)]

        rot = (1, -1)
        # performing rotation
        for rect in self.initial_piece_rects:
            rel = [(rect.topleft[dim] / self.tile_size[dim]) - core_coords[dim] for dim in range(2)]
            new_coords = [int((rel[(i+1) % 2] * rot[i] + core_coords[i]) * self.tile_size[i]) for i in range(len(rel))]
            rect.topleft = tuple(new_coords)

    def drop_piece(self, piece):
        # moves given piece to the lowest valid position
        while not self.touches_mass_or_bottom(piece):
            for rect in piece:
                rect.move_ip(0, self.tile_size[1])

    def touches_mass_or_bottom(self, piece):
        # checks to ensure a given piece configuration doesn't hit the lower mass (or bottom if no mass)
        bottom_height = self.top_left_corner[1] + self.tile_size[1]*self.grid_size[1]

        for self_rect in piece:
            if self_rect.bottom > bottom_height or self_rect in self.initial_mass:
                return True
        return False

    def touches_sides(self, piece):
        # checks to ensure a given piece configuration doesn't hit the play grid edge
        left_edge = self.top_left_corner[0]
        right_edge = self.top_left_corner[0] + self.tile_size[0]*self.grid_size[0]

        for self_rect in piece:
            if self_rect.left < left_edge or self_rect.right > right_edge or self_rect in self.initial_mass:
                return True
        return False
