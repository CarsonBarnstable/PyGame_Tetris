from TileInformation import get_random_tile_attributes
import pygame


class Piece:
    # Single instance of a Tile

    def __init__(self, screen, tlc, grid_size, tile_size):
        # Initializes a single Piece

        # Initialize Basic Visual Variables
        self.screen = screen
        self.top_left_corner = tlc
        self.grid_size = grid_size
        self.tile_size = tile_size

        # Setting initializing Variables
        piece_info = get_random_tile_attributes()
        self.spawn_position = (4, -2)
        self.vertical_offset = 0

        # Initialize Tile Attributes
        self.tile_color = pygame.Color(piece_info[0])
        relative_square_positions = piece_info[1]
        self.can_rotate = piece_info[2]

        # Setting up Piece Rects
        self.rects = self.set_up_rects(relative_square_positions)

    def draw(self):
        # Draws the Piece at its position

        for rectangle in self.rects:
            pygame.draw.rect(self.screen, self.tile_color, rectangle)

    def fall(self, movement_amount):
        # Moves Vertical Offset by set Amount
        self.vertical_offset = self.vertical_offset + movement_amount
        if self.vertical_offset >= self.tile_size[1]:
            self.vertical_offset = self.vertical_offset % self.tile_size[1]
            for rect in self.rects:
                rect.move_ip(0, self.tile_size[1])

    def shift(self, horizontal_shift):
        for rect in self.rects:
            rect.move_ip(horizontal_shift, 0)

    def rotate(self, matrix):
        centre_point = self.rects[0].topleft

        core_coords = []
        for dimension in range(len(centre_point)):
            core_coords.append(centre_point[dimension] / self.tile_size[dimension])

        for rect in self.rects:
            relative_pos = []
            for dim in range(2):
                relative_pos.append((rect.topleft[dim] / self.tile_size[dim]) - core_coords[dim])

            new_coords = []
            for i in range(len(relative_pos)):
                new_coords.append(int((relative_pos[(i + 1) % 2] * matrix[i] + core_coords[i]) * self.tile_size[i]))

            rect.topleft = tuple(new_coords)

    def pop_down(self):
        for rect in self.rects:
            rect.move_ip(0, self.tile_size[1])

    def force_down_to(self, mass):
        for row_repeat in range(self.grid_size[1]):
            for rect in self.rects:
                rect.move_ip(0, self.tile_size[1])
            if self.touches_mass_or_bottom(mass):
                break

    def snap_up_to_grid(self):
        for rect in self.rects:
            rect.move_ip(0, -1*self.tile_size[1])
            rect.move_ip((0, -1*(rect.top % self.tile_size[1])))

    def set_up_rects(self, list_of_positions):
        # Turns coordinate pairs into individual rectangles

        list_of_rects = []
        coordinates = []

        for pair in list_of_positions:
            temp_pair = []
            for d in range(2):
                temp_pair.append(self.top_left_corner[d] + self.tile_size[d]*(self.spawn_position[d] + pair[d]))
            coordinates.append(temp_pair)

        for top_left_coords in coordinates:
            list_of_rects.append(pygame.Rect(top_left_coords, self.tile_size))

        return list_of_rects

    def touches_mass_or_bottom(self, mass):
        does_touch = False
        bottom_height = self.top_left_corner[1] + self.tile_size[1]*self.grid_size[1]

        for self_rect in self.rects:

            if self_rect.bottom > bottom_height:
                does_touch = True

            for mass_rect in mass:
                if self_rect.colliderect(mass_rect[1]):
                    does_touch = True

        if does_touch:
            self.snap_up_to_grid()

        return does_touch

    def touches_sides(self, mass):
        left_edge = self.top_left_corner[0]
        right_edge = self.top_left_corner[0] + self.tile_size[0]*self.grid_size[0]

        for self_rect in self.rects:
            if self_rect.left < left_edge or self_rect.right > right_edge:
                return True
            if any(self_rect.colliderect(mass_rect[1]) for mass_rect in mass):
                return True

        return False

    def rotation_was_illegal(self, matrix, mass):
        was_illegal = False

        left_edge = self.top_left_corner[0]
        right_edge = self.top_left_corner[0] + self.tile_size[0]*self.grid_size[0]
        bottom_edge = self.top_left_corner[1] + self.tile_size[1]*self.grid_size[1]

        for rect in self.rects:

            if rect.left < left_edge or rect.right > right_edge or rect.bottom > bottom_edge:
                was_illegal = True

            for piece in mass:
                if rect.colliderect(piece[1]):
                    was_illegal = True

        if not self.can_rotate:
            for repeat in range(3):
                self.rotate(matrix)

        return was_illegal

    def get_rects(self):
        return self.rects

    def get_centre_x(self):
        return self.rects[0][0] / self.tile_size[0]

    def get_y(self):
        return self.rects[0][1]

    def get_info(self):
        return self.tile_color, self.rects
