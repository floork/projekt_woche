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
    pc_hit,
    pc_miss,
    pc_score,
    pc_shoot,
    place_ship,
    player_board,
    player_hit,
    player_miss,
    player_score,
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
    hit_miss = create_board(PLAYINGBOARDSIZE + 1)
    for element in pc_hit:
        hit_miss[element] = "hit"
    for element in pc_miss:
        hit_miss[element] = "miss"
    for j in range(PLAYINGBOARDSIZE + 1):
        spalten.clear()
        if j:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    if player_board.get((num_to_letter(j - 1), i - 1)):
                        spalten.append("🚢")
                    else:
                        spalten.append(" ")
                    if hit_miss.get(
                        (num_to_letter(j - 1), i - 1)
                    ) == "hit" and player_board.get(
                        (num_to_letter(j - 1), i - 1)
                    ):
                        spalten.remove("🚢")
                        spalten.append("🔥")
                    elif hit_miss.get(
                        (num_to_letter(j), i)
                    ) == "miss" and not player_board.get(
                        (num_to_letter(j - 1), i - 1)
                    ):
                        spalten.remove(" ")
                        spalten.append("💦")
                else:
                    spalten.append(num_to_letter(j - 1))
        else:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    spalten.append(i - 1)
                else:
                    spalten.append("")
        zeilen.append(spalten[0:-1])

    temp = Element("player_board")
    temp.element.innerHTML = table(zeilen)


def board_hit_miss_pc():
    """creates the hit miss board"""
    spalten = []
    zeilen = []
    hit_miss = create_board(PLAYINGBOARDSIZE + 1)
    for element in player_hit:
        hit_miss[element] = "hit"
    for element in player_miss:
        hit_miss[element] = "miss"
    for j in range(PLAYINGBOARDSIZE + 1):
        spalten.clear()
        if j:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    if hit_miss.get((num_to_letter(j - 1), i - 1)) == "hit":
                        spalten.append("🔥")
                    elif hit_miss.get((num_to_letter(j - 1), i - 1)) == "miss":
                        spalten.append("💦")
                    else:
                        spalten.append(" ")
                else:
                    spalten.append(num_to_letter(j - 1))
        else:
            for i in range(PLAYINGBOARDSIZE + 2):
                if i:
                    spalten.append(i - 1)
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
    global player_score, pc_score
    letter = Element("shoot_letter").element.value
    number = Element("shoot_number").element.value
    if player_shoot(Coordinate(letter, number), pc_board):
        player_score += 1
    if pc_shoot(player_board):
        pc_score += 1
    score_pc = Element("score_1")
    score_pc.element.innerHTML = pc_score
    score_player = Element("score_2")
    score_player.element.innerHTML = player_score
    board_player()
    board_hit_miss_pc()
    winning_condition()


def new_game():
    """starts a new game"""
    reset_fields()
    for i in range(2, 6):
        var = Element("laenge_" + str(i))
        val = var.element.value
        val = int(val)
        set_ships(val, i, pc_board)
        if Element("auto_place").element.checked:
            set_ships(val, i, player_board)
    Element("shoot_letter").element.disabled = False
    Element("shoot_number").element.disabled = False
    Element("shoot_ships").element.disabled = False
    board_player()
    board_hit_miss_pc()
    print(pc_board)


def reset_fields():
    """resets the board"""
    global player_board, pc_board, player_score, pc_score
    player_hit.clear()
    player_miss.clear()
    player_score = 0
    pc_hit.clear()
    pc_miss.clear()
    pc_score = 0
    player_board = clear_board(PLAYINGBOARDSIZE, player_board)
    pc_board = clear_board(PLAYINGBOARDSIZE, pc_board)
    Element("score_1").element.innerHTML = 0
    Element("score_2").element.innerHTML = 0
    board_player()
    board_hit_miss_pc()
    Element("winner").element.innerHTML = "<b>-</b>"
    Element("winner").element.style.backgroundColor = ""
    Element("shoot_letter").element.disabled = True
    Element("shoot_number").element.disabled = True
    Element("shoot_ships").element.disabled = True


def winning_condition():
    bod = Element("winner")
    player_ships = [k for k, v in player_board.items() if v == True]
    pc_ships = [k for k, v in pc_board.items() if v == True]
    if len(player_ships) == len(pc_hit):
        bod.element.innerHTML = (
            "Der Feind gewinnt!"
        )
        bod.element.style.backgroundColor="violet"
        Element("shoot_letter").element.disabled = True
        Element("shoot_number").element.disabled = True
        Element("shoot_ships").element.disabled = True
    elif len(pc_ships) == len(player_hit):
        bod.element.innerHTML = (
            "Der Spieler gewinnt!"
        )
        bod.element.style.backgroundColor="violet"
        Element("shoot_letter").element.disabled = True
        Element("shoot_number").element.disabled = True
        Element("shoot_ships").element.disabled = True


# so that the tabels are visable by default
board_player()
board_hit_miss_pc()
