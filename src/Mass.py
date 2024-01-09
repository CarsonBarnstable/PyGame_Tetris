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

    def deal_with_full_rows(self, full_grid_size, tile_size):
        # Setup
        height = tile_size[1]
        row_counter_accumulator = {row_i*height: {'count': 0, 'pieces': []} for row_i in range(full_grid_size[1])}

        # Indexing and Taking Note of All Pieces
        for piece in self.pieces:
            y_val = piece[1][1]
            if y_val < 0:  # vertical overflow
                return -1
            row_counter_accumulator[y_val]['count'] += 1
            row_counter_accumulator[y_val]['pieces'].append(piece)

        # Determining all Full Rows
        full_rows = []
        for y_height, row_details in row_counter_accumulator.items():
            if row_details['count'] == full_grid_size[0]:
                full_rows.append(y_height)

        # Dealing with Full Rows (from Bottom Up)
        for full_row_y_height in sorted(full_rows, reverse=True):
            # Deleting Elements from Full Row
            for piece in row_counter_accumulator[full_row_y_height]['pieces']:
                self.pieces.remove(piece)
            # and Shifting *Above* Elements Down
            for row_i in range(full_grid_size[1]-1):
                if row_i*tile_size[1] >= full_row_y_height:
                    break  # onto next full row
                for piece in row_counter_accumulator[row_i*height]['pieces']:
                    piece[1][1] += tile_size[1]

        # Returning the Number of Full Rows
        return len(full_rows)
