from fltk import ligne, cercle, polygone, texte, rectangle
from constants import all_players, all_lines, line_size, player_size, all_polygons, game, all_qix, all_sparx, \
    sparx_size, all_obstacles, obstacle_size, all_checkbox, checkbox_size, all_apples, apple_size, window_width, \
    surface_size


def draw_pause_save():
    x, y = window_width//2 - surface_size//2, 10
    texte(x, y, "press 'p' to pause the game", couleur='white', taille=20)
    texte(x, y+40, "press 'n' to save the game", couleur='white', taille=20)


def draw_all() -> None:
    """ draw everything """
    draw_polygons()
    draw_lines()
    draw_sparx()
    draw_player()
    draw_qix()
    draw_area()
    x, y = 20, 60
    for player in all_players:
        is_p1 = player["creative_touch"]=="Return"
        draw_missing_lives(player, is_p1, x, y)
        draw_score(player, is_p1, x, y+40)
        draw_wins(player, is_p1, x, y+80)
        y = 60
        x = window_width//2 + surface_size//2 + 20
    draw_apples()
    draw_obstacles()
    draw_pause_save()


def draw_apples() -> None:
    """ draw all apples """
    for apple in all_apples:
        cercle(apple[0], apple[1], apple_size, "red", remplissage="red")


def draw_area() -> None:
    """ draw the text with filled area percentage """
    x = 20
    y = 20
    area = 'area : ' + str(int(game['percentage_filled'])) + "%"
    texte(x, y, area, couleur='white', taille=20)


def draw_button(ax: int, ay: int, bx: int, by: int, text: str):
    """ draw a button """
    rectangle(ax, ay, bx, by, "grey", remplissage="grey")
    texte(ax + 10, ay + 10, text)


def draw_checkboxes(debut_x, debut_y):
    """ draw a checkbox """
    xa, ya = debut_x, debut_y

    # draw checkboxes
    for checkbox in all_checkbox.values():
        xb, yb = xa + checkbox_size, ya + checkbox_size
        if checkbox['is_checked']:
            rectangle(xa, ya, xb, yb, "white", epaisseur=7, remplissage="grey")
        else:
            rectangle(xa, ya, xb, yb, "white", epaisseur=7)
        y = ya + checkbox_size // 2 - 20
        x = xa + checkbox_size + 10
        texte(x, y, checkbox['text'], couleur='white', taille=20)
        ya += checkbox_size + 10

    text = "Modify more parameters on config.txt file"
    texte(xa, ya + 20, text, couleur='white', taille=20)


def draw_creative_lines(player) -> None:
    """ draw future lines if creative mode is enabled """
    for i in range(len(player['creative_lines_points']) - 1):
        xa, ya = player['creative_lines_points'][i]
        xb, yb = player['creative_lines_points'][i + 1]
        ligne(xa, ya, xb, yb, "white")
    
    # drawing the line to the player
    if player['creative_lines_points']:
        ligne(player['creative_lines_points'][-1][0], player['creative_lines_points'][-1][1], player['x'], player['y'], "white")


def draw_lines() -> None:
    """ draw all lines """
    for line in all_lines.values():
        ligne(line['a'][0], line['a'][1], line['b'][0], line['b'][1], "white", line_size)


def draw_missing_lives(player, is_p1, x, y) -> None:
    """ draw the text with player's missing lives """
    p = "p1" if is_p1 else "p2"
    lives = f"Lives {p} : {str(player['missing_lives'])}"
    texte(x, y, lives, couleur='white', taille=20)


def draw_obstacles() -> None:
    """draw all obstacles"""
    for obstacle in all_obstacles:
        cercle(obstacle[0], obstacle[1], obstacle_size, "gray", remplissage="gray")


def draw_player() -> None:
    """ draw the player """
    for player in all_players:
        if player['is_alive']:
            player_color = "yellow" if player["invincible_timer"] else "green"
            cercle(player['x'], player['y'], player_size, "white", remplissage=player_color)


def draw_polygons() -> None:
    """ draw all polygons """
    for i in range(len(all_polygons)):
        color = game['polygon_colors'][i]
        polygone(all_polygons[i], color, remplissage=color)


def draw_qix() -> None:
    """ draw all qix """
    for qix in all_qix:
        ligne(qix['x1'], qix['y1'], qix['x2'], qix['y2'], "red", epaisseur=10)


def draw_score(player, is_p1, x, y) -> None:
    """ draw the text with player's score """
    p = "p1" if is_p1 else "p2"
    score = f"Score {p} : {str(player['score'])}"
    texte(x, y, score, couleur='white', taille=20)


def draw_sparx() -> None:
    """ draw all sparx """
    for sparx in all_sparx:
        cercle(sparx['x'], sparx['y'], sparx_size, "blue", remplissage="blue")


def draw_wins(player, is_p1, x, y) -> None:
    """ draw the text with player's wins """
    p = "p1" if is_p1 else "p2"
    wins = f"Wins {p} : {str(player['wins'])}"
    texte(x, y, wins, couleur='white', taille=20)
