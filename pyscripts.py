"""
pyscript code der getrennt von den hauptcode ist
"""
from tabulate import tabulate

from main import (
    PLAYINGBOARDSIZE,
    Coordinate,
    Schiff,
    clear_board,
    create_board,
    num_to_letter,
    pc_board,
    pc_count,
    pc_hit,
    pc_miss,
    place_ship,
    player_board,
    player_count,
    player_hit,
    player_miss,
    player_shoot,
    set_ships,
)


def table(tabelle):
    """generates a html table"""
    return tabulate(tabelle, tablefmt="html")


def board_player():
    """creates the player board"""
    spalten = []
    zeilen = []
    for j in range(PLAYINGBOARDSIZE + 1):
        spalten.clear()
        if j:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    if player_board.get((num_to_letter(j), i)):
                        spalten.append("🛥")
                    else:
                        spalten.append(" ")
                else:
                    spalten.append(j - 1)
        else:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    spalten.append(num_to_letter(i - 1))
                else:
                    spalten.append(" ")
        zeilen.append(spalten[0:-1])

    temp = Element("player_board")
    temp.element.innerHTML = table(zeilen)


def board_hit_miss():
    """creates the hit miss board"""
    spalten = []
    zeilen = []
    hit_miss = create_board(PLAYINGBOARDSIZE)
    for element in player_hit:
        hit_miss[element] = "hit"
    for element in player_miss:
        hit_miss[element] = "miss"
    for j in range(PLAYINGBOARDSIZE + 1):
        spalten.clear()
        for i in range(PLAYINGBOARDSIZE + 2):
            if hit_miss.get((num_to_letter(j), i)) == "hit":
                spalten.append("❌")
            elif hit_miss.get((num_to_letter(j), i)) == "miss":
                spalten.append("⭕️")
            else:
                spalten.append(" ")
        zeilen.append(spalten[0:-1])

    temp = Element("hitmiss_board")
    temp.element.innerHTML = table(zeilen)


def ship_place():
    """places the ships"""
    start_letter = Element("start_letter").element.value
    start_number = Element("start_number").element.value
    end_letter = Element("end_letter").element.value
    end_number = Element("end_number").element.value
    start_point = Coordinate(start_letter, int(start_number))
    end_point = Coordinate(end_letter, int(end_number))
    place_ship(Schiff(start_point, end_point), player_board)


def ship_shoot():
    """shoots the ships"""
    letter = Element("shoot_letter").element.value
    number = Element("shoot_number").element.value
    player_shoot(Coordinate(letter, number), pc_board)


def new_game():
    """starts a new game"""
    reset_fields()
    for i in range(1, 5):
        var = Element("laenge_" + str(i))
        val = var.element.value
        val = int(val)
        set_ships(val, i, pc_board)
        if Element("auto_place").element.checked:
            set_ships(val, i, player_board)
    board_player()
    board_hit_miss()


def reset_fields():
    """resets the board"""
    global player_board, pc_board
    player_hit.clear()
    player_miss.clear()
    pc_hit.clear()
    pc_miss.clear()
    player_board = clear_board(PLAYINGBOARDSIZE, player_board)
    pc_board = clear_board(PLAYINGBOARDSIZE, pc_board)
    board_player()
    board_hit_miss()


# so that the tabels are visable by default
board_player()
board_hit_miss()
