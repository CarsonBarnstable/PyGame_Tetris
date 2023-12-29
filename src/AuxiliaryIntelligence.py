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

        for rotation_iteration in range(4):
            self.rotate_piece()

            for x_coord in range(self.grid_size[0]):
                pieces = []

                for piece in self.initial_piece_rects:
                    pieces.append(piece.move(x_coord * self.tile_size[0], 0))
                self.drop_piece(pieces)

                for piece in pieces:
                    piece.move_ip(0, -1*self.tile_size[1])

                if not self.touches_sides(pieces):
                    valid_mass = self.initial_mass + pieces
                    self.valid_masses[rotation_iteration, x_coord] = valid_mass

        return self.valid_masses

    def center_piece(self):
        prior_center = self.initial_piece_rects[0].topleft

        for rect in self.initial_piece_rects:
            rect.move_ip(-1*prior_center[0], -1*prior_center[1])

    def rotate_piece(self):
        rot_matrix = (1, -1)

        centre_point = self.initial_piece_rects[0].topleft

        core_coords = []
        for dimension in range(len(centre_point)):
            core_coords.append(centre_point[dimension] / self.tile_size[dimension])

        for rect in self.initial_piece_rects:
            relative_pos = []
            for dim in range(2):
                relative_pos.append((rect.topleft[dim] / self.tile_size[dim]) - core_coords[dim])

            new_coords = []
            for i in range(len(relative_pos)):
                new_coords.append(int((relative_pos[(i + 1) % 2] * rot_matrix[i] + core_coords[i]) * self.tile_size[i]))

            rect.topleft = tuple(new_coords)

    def drop_piece(self, piece):
        for row_repeat in range(self.grid_size[1]):
            for rect in piece:
                rect.move_ip(0, self.tile_size[1])
            if self.touches_mass_or_bottom(piece):
                break

    def touches_mass_or_bottom(self, piece):
        does_touch = False
        bottom_height = self.top_left_corner[1] + self.tile_size[1]*self.grid_size[1]

        for self_rect in piece:

            if self_rect.bottom > bottom_height:
                does_touch = True

            for mass_rect in self.initial_mass:
                if self_rect.colliderect(mass_rect):
                    does_touch = True

            if self_rect.top < self.top_left_corner[1]:
                does_touch = True

        return does_touch

    def snap_up_to_grid(self, piece):
        for rect in piece:
            rect.move_ip(0, -1*self.tile_size[1])
            rect.move_ip((0, -1*(rect.top % self.tile_size[1])))

    def touches_sides(self, piece):
        does_touch = False
        left_edge = self.top_left_corner[0]
        right_edge = self.top_left_corner[0] + self.tile_size[0]*self.grid_size[0]

        for self_rect in piece:
            if self_rect.left < left_edge or self_rect.right > right_edge:
                does_touch = True

            for mass_rect in self.initial_mass:
                if self_rect.colliderect(mass_rect):
                    does_touch = True

        return does_touch
