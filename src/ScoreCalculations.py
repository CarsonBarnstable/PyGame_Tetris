import pygame


def get_score(mass_rect_list, grid_size, tile_size, coefficients, move=None):
    full_rows = num_of_full_rows(mass_rect_list, grid_size, tile_size)
    bumpiness = bumpiness_index(mass_rect_list, grid_size, tile_size)
    dist_to_top = distance_to_top(mass_rect_list, grid_size, tile_size)
    overhangs = number_of_overhangs(mass_rect_list, grid_size, tile_size)
    percent = percent_of_mass_filled(mass_rect_list, grid_size, tile_size)

    resulting_score = calc_score(full_rows, bumpiness, dist_to_top, overhangs, percent, coefficients)
    if move:
        return resulting_score, move
    # else
    return resulting_score


def num_of_full_rows(mass, grid_size, tile_size):
    num = 0

    for y_index in range(grid_size[1]):
        row_y_value = y_index*tile_size[1]
        pieces_in_row = 0

        for rect in mass:
            if rect.top == row_y_value:
                pieces_in_row = pieces_in_row + 1

        if pieces_in_row == grid_size[0]:
            num = num + 1

    return num


def bumpiness_index(mass, grid_size, tile_size):
    top_rect_heights = {}
    total_bumpiness = 0

    for x_index in range(grid_size[0]):
        top_rect_heights[x_index * tile_size[0]] = grid_size[1] * tile_size[1]

    for rect in mass:
        top_rect_heights[rect.left] = min(top_rect_heights.get(rect.left), rect.top)

    for x_val in range(1, grid_size[0]):
        delta = abs(top_rect_heights.get(x_val * tile_size[0]) - top_rect_heights[(x_val - 1) * tile_size[0]])
        total_bumpiness = total_bumpiness + delta

    adjusted_bumpiness = total_bumpiness / tile_size[1]

    return adjusted_bumpiness


def distance_to_top(mass, grid_size, tile_size):
    min_y = grid_size[1] * tile_size[1]

    for rect in mass:
        if rect.top < min_y:
            min_y = rect.top

    dist = min_y / tile_size[1]

    return dist


def number_of_overhangs(mass, grid_size, tile_size):
    num_of_overhangs = 0

    for potential_top_rect in mass:
        needed_below_support = pygame.Rect(potential_top_rect.move(0, tile_size[1]))

        if potential_top_rect.bottom < grid_size[1] * tile_size[1]:
            if True not in [needed_below_support.top == rt.top and needed_below_support.left == rt.left for rt in mass]:
                num_of_overhangs = num_of_overhangs + 1

    return num_of_overhangs


def percent_of_mass_filled(mass, grid_size, tile_size):
    min_y = grid_size[1] * tile_size[1]

    for rect in mass:
        if rect.top < min_y:
            min_y = rect.top

    max_rects = ((grid_size[1] * tile_size[1] - min_y) / tile_size[1]) * grid_size[0]
    actual_rects = len(mass)

    return actual_rects / max_rects


def calc_score(full_rows, bumpiness, dist_to_top, overhangs, percent, coefficients):
    scores = {"full_rows": coefficients.get("full_rows", 0) * full_rows,
              "bumpiness": coefficients.get("bumpiness", 0) * bumpiness,
              "dist_to_top": coefficients.get("dist_to_top", 0) * dist_to_top,
              "overhangs": coefficients.get("overhangs", 0) * overhangs,
              "percent_filled": coefficients.get("percent_filled", 0) * percent}

    score = 0
    for key in scores.keys():
        piece_score = scores.get(key, 0)
        score = score + piece_score

    return score
