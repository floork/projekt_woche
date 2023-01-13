"""hauptcode des schiffeversenken"""

import random


class Coordinate:
    """defines the Coordinate"""

    def __init__(self, H: str, V: int):
        self.HOR: str = H
        self.VERT: int = V


class Schiff:
    """defines the Ship"""

    def __init__(self, f: Coordinate, l: Coordinate):
        self.first: Coordinate = f
        self.last: Coordinate = l


def create_board(groesse):
    """generate playing board"""
    brd = {}
    for i in range(groesse):
        for j in range(groesse):
            brd[(num_to_letter(i), j)] = False
    return brd


def clear_board(groesse, brd: dict):
    """generate playing board"""
    for i in range(groesse):
        for j in range(groesse):
            brd[(num_to_letter(i), j)] = False
    return brd


def num_to_letter(num: int):
    """converts numbers into letters and greater numbers to (ABC)"""
    if num < 26:
        buchstabe = chr(num + 65)
        return buchstabe

    buchstabe1 = num_to_letter(int(num / 26) - 1)
    num -= 26 * int(num / 26)
    buchstabe2 = num_to_letter(num)
    buchstaben = buchstabe1 + buchstabe2
    return buchstaben


def place_ship(new_ship: Schiff, board: dict):
    """places ship"""
    # set's horizontal ship
    if new_ship.first.HOR == new_ship.last.HOR:
        line = new_ship.first.HOR
        stard = new_ship.first.VERT
        ende = new_ship.last.VERT
        leng = ende - stard
        cut = 1

        # tests whether a ship crosses another
        for i in range(leng):
            if test_space((line, stard + i), board):
                continue
            cut = 0

        # ship get's set in dictionary
        if cut:
            for i in range(leng):
                board[(line, stard + i)] = True
            return board

        return False

    # set's vertical ship
    if new_ship.first.VERT == new_ship.last.VERT:
        spalte = new_ship.first.VERT
        stard = letter_to_num(new_ship.first.HOR)
        ende = letter_to_num(new_ship.last.HOR)
        leng = ende - stard
        cut = 1

        # tests whether a ship crosses another
        for i in range(leng):
            if test_space((num_to_letter(stard + i), spalte), board):
                continue
            cut = 0
        # ship get's set in dictionary
        if cut:
            for i in range(leng):
                board[(num_to_letter(stard + i), spalte)] = True
            return board
        return False


def test_space(cell, board: dict):
    """tests key in dic and true"""
    return cell in board and not board.get(cell)


def letter_to_num(letters: str):
    """converts letter strings to numbers"""
    i = 0
    numb = 0
    for letter in reversed(letters):
        numb += (ord(letter) - 64) * 26**i
        i += 1
    return numb - 1


def ignore_num(zkette: str):
    """ignores input numbers"""
    newstring = ""
    abc = set()
    zkette.upper()
    for i in range(26):
        abc.add(chr(65 + i))
    for character in zkette:
        if character in abc:
            newstring += character
    return newstring


def ignore_float(numb: float):
    """useless"""
    return int(numb)


def get_random_field():
    """gets a random field"""
    board = create_board(PLAYINGBOARDSIZE)
    field_list = list(board.keys())
    field = random.choice(field_list)
    return field


def pc_shoot(dic: dict):
    """function to shoot a boat"""
    # empty list to store already shot fields
    already_shot: list = []
    field = get_random_field()

    if field in already_shot:
        pc_shoot(dic)
    # check if ship is on field and shoot it
    if dic.get(field):
        hit = dic[field] = True
        pc_hit.append(field)
        return hit, 1
    miss = dic[field] = False
    pc_miss.append(field)
    return miss


def player_shoot(
    field: Coordinate,
    dic: dict,
):
    """player shoots"""
    hor = field.HOR
    vert = int(field.VERT)
    new_field = (hor.upper(), vert)
    if dic.get(new_field):
        hit = dic[new_field] = True
        player_hit.append(new_field)
        return hit, 1
    miss = dic[new_field] = False
    player_miss.append(new_field)
    return miss


def set_ships(frequency: int, lenght: int, board: dict):
    """places the ships for the pc"""
    while frequency != 0:
        start_point = get_random_field()
        get_direction = random.choice(start_point)

        # vertical
        if get_direction == start_point[0]:
            if lenght == 1:
                end_point = get_direction
                place_ship(
                    Schiff(
                        Coordinate(start_point[0], start_point[1]),
                        Coordinate(end_point, start_point[1]),
                    ),
                    board,
                )
            else:
                end_point = letter_to_num(get_direction) + lenght
                if end_point < PLAYINGBOARDSIZE:
                    end_point = num_to_letter(end_point)
                    place_ship(
                        Schiff(
                            Coordinate(start_point[0], start_point[1]),
                            Coordinate(end_point, start_point[1]),
                        ),
                        board,
                    )
            frequency -= 1

        # horizontal
        elif get_direction == start_point[1]:
            if lenght == 1:
                end_point = get_direction
                place_ship(
                    Schiff(
                        Coordinate(start_point[0], start_point[1]),
                        Coordinate(start_point[0], end_point),
                    ),
                    board,
                )
            else:
                end_point = get_direction + lenght
                if end_point < PLAYINGBOARDSIZE:
                    place_ship(
                        Schiff(
                            Coordinate(start_point[0], start_point[1]),
                            Coordinate(start_point[0], end_point),
                        ),
                        board,
                    )
            frequency -= 1


# GLOBAL VALUES
PLAYINGBOARDSIZE = 10
player_hit: list = []
player_miss: list = []
player_board = create_board(PLAYINGBOARDSIZE)
player_score = 0
pc_hit: list = []
pc_miss: list = []
pc_board = create_board(PLAYINGBOARDSIZE)
pc_score = 0
