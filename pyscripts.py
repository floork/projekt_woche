"""
pyscript code der getrennt von den hauptcode ist
"""
from pyscript import Element # type: ignore
from tabulate import tabulate

from main import (
    PLAYINGBOARDSIZE,
    Coordinate,
    Schiff,
    create_board,
    num_to_letter,
    pc_count,
    place_ship,
    player_board,
    player_count,
    player_hit,
    player_miss,
    player_shoot,
    set_ships_pc,
    set_ships_player,
)


def table(tabelle):
    """generates a html table"""
    return tabulate(tabelle, tablefmt="html")


def board_player():
    """creates the player board"""
    spalten: list = []
    zeilen: list = []
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
    spalten: list = []
    zeilen: list = []
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


# WICHTIG: Tabellen muessen in funktionen sein da sonst dopplungen auftreten koennten
board_player()
board_hit_miss()


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
    letter = Element("shoot_letter").value
    number = Element("shoot_number").value
    player_shoot(Coordinate(letter, number), player_board)
    label_pc = Element("score_1")
    label_player = Element("score_2")
    label_pc.element.innerHTML = pc_count
    label_player.element.innerHTML = player_count


# ERROR: infinite loop
def loop_fields():
    """loops through the input fields and places the ships"""
    create_board(PLAYINGBOARDSIZE)
    for i in range(1, 5):
        var = Element("laenge_" + str(i))
        val = var.element.value
        set_ships_pc(val, i)
        if Element("auto_place").element.checked:
            set_ships_player(val, i)


def reset_fields():
    """resets the board"""
    board_player()
    board_hit_miss()
