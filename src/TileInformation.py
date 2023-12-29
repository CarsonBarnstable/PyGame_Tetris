import random


def get_i():
    # Information for "I" Piece
    color = "light blue"
    positions = [(0, 0), (-1, 0), (1, 0), (2, 0)]
    does_rotate = True
    return [color, positions, does_rotate]


def get_j():
    # Information for "J" Piece
    color = "blue"
    positions = [(0, 0), (-1, 0), (1, 0), (-1, -1)]
    does_rotate = True
    return [color, positions, does_rotate]


def get_l():
    # Information for "L" Piece
    color = "orange"
    positions = [(0, 0), (-1, 0), (1, 0), (1, -1)]
    does_rotate = True
    return [color, positions, does_rotate]


def get_o():
    # Information for "O" Piece
    color = "yellow"
    positions = [(0, 0), (1, 0), (0, -1), (1, -1)]
    does_rotate = False
    return [color, positions, does_rotate]


def get_s():
    # Information for "S" Piece
    color = "lime green"
    positions = [(0, 0), (-1, 0), (0, -1), (1, -1)]
    does_rotate = True
    return [color, positions, does_rotate]


def get_z():
    # Information for "Z" Piece
    color = "red"
    positions = [(0, 0), (1, 0), (0, -1), (-1, -1)]
    does_rotate = True
    return [color, positions, does_rotate]


def get_t():
    # Information for "T" Piece
    color = "purple"
    positions = [(0, 0), (-1, 0), (1, 0), (0, -1)]
    does_rotate = True
    return [color, positions, does_rotate]


all_tile_attributes = {"I": get_i(), "J": get_j(), "L": get_l(), "O": get_o(), "S": get_s(), "Z": get_z(), "T": get_t()}


def get_random_tile_attributes():
    # Gets all the information for a randomized tile
    return all_tile_attributes[random.choice(["I", "J", "L", "O", "S", "Z", "T"])]
