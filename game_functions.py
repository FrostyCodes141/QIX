from database import load_played_game
from fltk import attend_clic_gauche, ferme_fenetre, image, texte
from draw_functions import draw_button, draw_all, draw_checkboxes
from obstacles import update_obstacles, generate_obstacles, create_checkbox, verify_checkbox, generate_apples, \
    update_apples
from player import update_player, create_player
from lines import create_line
from qix import update_qix, create_qix
from sparx import create_sparx, update_sparx
from constants import *


def display_menu() -> None:
    """ display the menu """
    # play button
    pax = window_width // 2 - 100
    pay = window_height // 2 - 100
    pbx = pax + len("Play") * 16 + 20
    pby = pay + 50
    draw_button(pax, pay, pbx, pby, "Play")
    # quit button
    qax = window_width // 2 - 100
    qay = pby + 10
    qbx = qax + len("Quit") * 16 + 20
    qby = qay + 50
    draw_button(qax, qay, qbx, qby, "Quit")
    # option button
    oax = window_width // 2 - 100
    oay = qby + 10
    obx = oax + len("Options") * 16 + 20
    oby = oay + 50
    draw_button(oax, oay, obx, oby, "Options")
    # load game button
    lax = window_width // 2 - 100
    lay = oby + 10
    lbx = lax + len("Load game") * 16 + 20
    lby = lay + 50
    draw_button(lax, lay, lbx, lby, "Load game")
    # controls button
    cax = window_width // 2 - 100
    cay = lby + 10
    cbx = cax + len("Controls") * 16 + 20
    cby = cay + 50
    draw_button(cax, cay, cbx, cby, "Controls")
    # get player coordinates
    px, py = attend_clic_gauche()
    if pax <= px <= pbx and pay <= py <= pby:
        game["is_playing"] = True
        launch_game()
    elif qax <= px <= qbx and qay <= py <= qby:
        ferme_fenetre()
        save_parameters()
        quit()
    elif oax <= px <= obx and oay <= py <= oby:
        game["option_menu"] = True
    elif lax <= px <= lbx and lay <= py <= lby:
        game['is_playing'] = True
        load_played_game()
    elif cax <= px <= cbx and cay <= py <= cby:
        game['controls_menu'] = True


def display_option_menu() -> None:
    """ display the option menu """
    # checkboxes
    draw_checkboxes(25, 25)
    # back button
    bax = window_width - len("Back") * 16 - 40
    bay = 10
    bbx = bax + len("Back") * 16 + 20
    bby = bay + 50
    draw_button(bax, bay, bbx, bby, "Back")
    # get player coordinates
    px, py = attend_clic_gauche()
    verify_checkbox(px, py, 25, 25)
    if bax <= px <= bbx and bay <= py <= bby:
        game["option_menu"] = False


def display_controls_menu() -> None:
    x, y = window_width//2, window_height//2 - 100
    image(x, y, "keys.png")
    # legend
    x -= 150
    y += 200
    texte(x, y, "Red : movement", couleur="white", taille=20)
    y += 40
    texte(x, y, "Green : creative mode", couleur="white", taille=20)
    y += 40
    texte(x, y, "Blue : bonus speed", couleur="white", taille=20)
    # back button
    bax = window_width - len("Back") * 16 - 40
    bay = 10
    bbx = bax + len("Back") * 16 + 20
    bby = bay + 50
    draw_button(bax, bay, bbx, bby, "Back")
    # get player coordinates
    px, py = attend_clic_gauche()
    if bax <= px <= bbx and bay <= py <= bby:
        game["controls_menu"] = False


def do_updates() -> None:
    """ update the game and draw everything """
    # drawing graphic stuff
    draw_all()

    # updating the game
    if not game['is_paused']:
        update_game()
        if all(not player['is_alive'] for player in all_players):
            restart_game()


def enable_checkbox() -> None:
    """ adding_checkbox"""
    all_checkbox["two_players"] = create_checkbox("two_players", "Two players ?", int(saved_parameters["two_players"]))
    all_checkbox["obstacles"] = create_checkbox("obstacles", "Obstacles ?", int(saved_parameters["obstacles"]))
    all_checkbox["bonus"] = create_checkbox("bonus", "Bonus ?", int(saved_parameters["bonus"]))
    all_checkbox["more_enemies"] = create_checkbox("more_enemies", "More enemies over time ?", int(saved_parameters["more_enemies"]))
    all_checkbox["speed_increase"] = create_checkbox("speed_increase", "Enemies speed increases over time ?", int(saved_parameters["speed_increase"]))


def init_game_parameters():
    game['surface_filled'] = 0
    game['percentage_filled'] = 0
    game['line_id'] = 3
    game['has_win'] = False
    game['polygon_colors'] = []
    game['additional_speed'] = 0
    game['is_playing'] = False
    game['qix_amount'] = 1
    game['sparx_amount'] = 2
    game['option_menu'] = False
    game['controls_menu'] = False
    game['is_paused'] = False


def launch_game() -> None:
    """ launch the game, first create the borders, then the player"""
    # creating borders of the game
    x = window_width // 2 - surface_size // 2
    y = window_height // 2 - surface_size // 2
    all_lines[0] = create_line(0, (x, y), (x + surface_size, y), "Up", True, 3, 1)
    all_lines[1] = create_line(1, (x, y), (x, y + surface_size), "Left", True, 2, 0)
    y += surface_size
    all_lines[2] = create_line(2, (x, y), (x + surface_size, y), "Down", True, 3, 1)
    x += surface_size
    all_lines[3] = create_line(3, (x, y - surface_size), (x, y), "Right", True, 2, 0)

    # when player is not in a line
    create_line(-1, (0, 0), (0, 0), "None", False, -1, -1)

    # getting all possible x coordinates for each player
    n_players = 2 if all_checkbox['two_players']['is_checked'] else 1
    left_x = all_lines[2]['a'][0]
    line_length = all_lines[2]['b'][0] - left_x
    segments_size = line_length // (n_players+1)
    x_coords = [left_x + i*segments_size for i in range(n_players+2)][1:-1]

    # creating player
    for i in range(n_players):
        all_players.append(create_player(i, x_coords[i], y, player_velocity, False, not i%2))

    # generating obstacles randomly
    if all_checkbox['obstacles']['is_checked']:
        generate_obstacles()
    if all_checkbox['bonus']['is_checked']:
        generate_apples()

    # generate qix
    for _ in range(game['qix_amount']):
        all_qix.append(create_qix())
    
    # generate sparx
    lines = [1, 3]
    sparx_per_line = [game['sparx_amount'] // 2] * 2
    sparx_per_line[0] += 1 if game['sparx_amount'] % 2 else 0
    y_coords = (get_segments(all_lines[1], sparx_per_line[0])[1:-1], get_segments(all_lines[3], sparx_per_line[1])[1:-1])
    for i in range(game['sparx_amount']):
        line_id = lines[i%2]
        x = all_lines[line_id]['a'][0]
        y = y_coords[i%2][i//2]
        direction = "down" if (len(all_sparx)//2) %2 else "up"
        all_sparx.append(create_sparx(x, y, direction, line_id))


def get_segments(studied_line, n):
    a_coord = studied_line['a'][1]
    line_length = studied_line['b'][1] - a_coord
    segments_size = line_length // (n+1)
    return [a_coord + i*segments_size for i in range(n+2)]


def next_level() -> None:
    """ pass to next level (relaunch the game with faster enemies) """
    # reset parameters to keep
    all_scores = [player['score'] for player in all_players]
    all_wins = [player['wins'] for player in all_players]
    is_playing = game['is_playing']
    add_speed = game['additional_speed'] + 1
    if all_checkbox["more_enemies"]['is_checked']:
        sparx_amount = game['sparx_amount'] + (add_speed//2)
        qix_amount = game['qix_amount'] + (add_speed//3)

    # reset the game
    restart_game()

    # keeping some parameters
    game['is_playing'] = is_playing
    game['additional_speed'] = add_speed
    if all_checkbox["more_enemies"]['is_checked']:
        game['sparx_amount'] = sparx_amount
        game['qix_amount'] = qix_amount

    # launch the game again
    launch_game()

    if len(all_scores) == 1:
        for i, player in enumerate(all_players):
            player['score'] = all_scores[i]
    else:
        score_p1, score_p2 = all_scores
        if score_p1 > score_p2:
            all_wins[0] += 1
        elif score_p2 > score_p1:
            all_wins[1] += 1
    for i, player in enumerate(all_players):
        player['wins'] = all_wins[i]


def restart_game():
    all_lines.clear()
    all_polygons.clear()
    all_players.clear()
    all_qix.clear()
    all_sparx.clear()
    all_obstacles.clear()
    all_apples.clear()
    game.clear()
    init_game_parameters()


def save_parameters():
    with open("config.txt", "w") as file:
        for k in saved_parameters:
            if k in all_checkbox:
                saved_parameters[k] = int(all_checkbox[k]['is_checked'])
            file.write(f"{k}:{saved_parameters[k]}\n")


def update_game() -> None:
    """ updating game objects (player, qix, sparx) """
    for player in all_players:
        if player['is_alive']:
            update_player(player)
    for qix in all_qix:
        update_qix(qix)
    for sparx in all_sparx:
        update_sparx(sparx)
    update_obstacles()
    update_apples()
