from checking_functions import get_line, test_pos, check_movement_allowed, get_line_collision, \
    can_add_surface, invalid_point, position_test, entity_pos, check_player_in_line, respawn_player, remove_life, \
    point_in_polygon
from constants import all_players, bonus_speed, all_polygons
from draw_functions import draw_creative_lines
from fltk import touche_pressee
from lines import update_lines, add_surface


def add_creative_point(direction: str, player) -> None:
    """ if the player changes of direction and started drawing, we add the point to creative_lines_points """
    if player['last_direction'] != direction and player['on_drawing_area']:
        player['creative_lines_points'].append((player['x'], player['y']))


def check_creative_lines_collision(player, player2, creative_line_points) -> None:
    """ check if the player is touching a line he is drawing """
    crl = creative_line_points.copy()
    if player != player2:
        crl.append((player2['x'], player2['y']))
    for i in range(len(crl) - 1):
        a, b = crl[i], crl[i + 1]
        h = a[1] == b[1]
        v = a[0] == b[0]
        # if the player is touching a line he is drawing, we respawn him and remove a life
        # a and b are the points of the line and h and v are booleans to know if the line is horizontal or vertical
        if check_player_in_line({'a': a, 'b': b, 'is_horizontal': h, 'is_vertical': v}, player):
            respawn_player(player)
            remove_life(player)
            break


def create_player(id_player: int, x: int, y: int, velocity: int, creating: bool, p1=True):
    """ create a player """
    return {
        'id': id_player,
        'x': x,
        'y': y,
        'velocity': velocity,
        'creating': creating,
        'last_direction': '',
        'first_creative_line_id': -1,
        'first_creative_pos': (0, 0),
        'missing_lives': 3,
        'is_alive': True,
        'creative_lines_points': [],
        'on_drawing_area': False,
        'touch_mapping': {"Up": "Up" if p1 else "z", "Down": "Down" if p1 else "s", "Left": "Left" if p1 else "q",
                          "Right": "Right" if p1 else "d"},
        'creative_touch': "Return" if p1 else "space",
        'bonus_speed_touch': "m" if p1 else "f",
        'bonus_speed': 0,
        'invincible_timer': 0,
        'score': 0,
        'wins': 0
    }


def invalid_player(player2):
    x, y = entity_pos(player2)
    line = get_line(x, y, check_active=False)
    if line is not None and not line['is_active']:
        return True
    return point_in_polygon(x, y, all_polygons[-1])


def creative_actions(player) -> None:
    """ update player movement and check if the player comes back on a line """

    if not player['on_drawing_area'] and touche_pressee(player['bonus_speed_touch']):
        player['bonus_speed'] = bonus_speed

    update_creative_movement(player)
    draw_creative_lines(player)

    # getting the line the player is currently on, get empty dict if the player is not on a line
    line = get_line_collision(player)

    # checking if the player as gone into the drawing area
    if not player['on_drawing_area'] and not line:
        player['on_drawing_area'] = True
        player['creative_lines_points'].append(player['first_creative_pos'])
    else:
        player['first_creative_pos'] = entity_pos(player)

    # if the player is on a line and has gone into the drawing area, we disable creative mode
    if line and player['on_drawing_area']:
        disable_creative_mode(line, player)
        for player2 in all_players:
            if player2 != player and invalid_player(player2):
                respawn_player(player2)
                remove_life(player2)

    if player['on_drawing_area'] and invalid_point(player['x'], player['y']):
        replace_player(player)

    # if the player started to draw, we check if he is not touching a line he is drawing
    for player2 in all_players:
        crl = player2['creative_lines_points']
        if crl:
            check_creative_lines_collision(player, player2, crl)


def disable_creative_mode(line, player):
    # updating players information
    player['actual_line_id'] = line['id']
    player['creating'] = False

    player['on_drawing_area'] = False

    # placing the player on the line he touched
    if line['is_horizontal']:
        player['y'] = line['a'][1]
    elif line['is_vertical']:
        player['x'] = line['a'][0]

    if can_add_surface(player):
        add_surface(line, player)
        update_lines()
        player['bonus_speed'] = 0
    player['creative_lines_points'].clear()


def get_player_actual_line(player):
    xp, yp = entity_pos(player)
    l = get_line(xp, yp)
    if l is None:
        replace_player(player)
        l = get_line(xp, yp)
        player['x'] = xp
        player['y'] = yp
    return l


def normal_actions(player) -> None:
    """ update player movement when creative mode is disabled """
    update_player_position(player)


def replace_player(player) -> None:
    """ place the player on the nearest line """
    x, y = entity_pos(player)
    i = 0
    test = None
    while test is None:
        i += 1
        test = test_pos(x, y, i, i)
    l, c = test
    player['x'] = x + l
    player['y'] = y + c


def update_creative_movement(player) -> None:
    """ update player position when creative mode is enabled """
    u, d, l, r = player['touch_mapping']['Up'], player['touch_mapping']['Down'], player['touch_mapping']['Left'], \
                    player['touch_mapping']['Right']
    velocity = player['velocity']
    velocity += player['bonus_speed'] if player['on_drawing_area'] else 0

    if touche_pressee(u) and check_movement_allowed("Up", player):
        add_creative_point("Up", player)
        player['y'] -= velocity
        player['last_direction'] = "Up"
    elif touche_pressee(d) and check_movement_allowed("Down", player):
        add_creative_point("Down", player)
        player['y'] += velocity
        player['last_direction'] = "Down"
    elif touche_pressee(r) and check_movement_allowed("Right", player):
        add_creative_point("Right", player)
        player['x'] += velocity
        player['last_direction'] = "Right"
    elif touche_pressee(l) and check_movement_allowed("Left", player):
        add_creative_point("Left", player)
        player['x'] -= velocity
        player['last_direction'] = "Left"


def update_player_position(player) -> None:
    """ make the player move """
    u, d, l, r = player['touch_mapping']['Up'], player['touch_mapping']['Down'], player['touch_mapping']['Left'], \
        player['touch_mapping']['Right']
    if touche_pressee(u):
        player['y'] -= position_test("up", player)
    elif touche_pressee(d):
        player['y'] += position_test("down", player)
    elif touche_pressee(l):
        player['x'] -= position_test("left", player)
    elif touche_pressee(r):
        player['x'] += position_test("right", player)


def update_player(player) -> None:
    """ updating player information """
    if player['invincible_timer']:
        player['invincible_timer'] -= 1
    
    if touche_pressee(player["creative_touch"]) and not player['creating']:
        # enable creative mode
        player["creating"] = True
        player['first_creative_line_id'] = get_player_actual_line(player)['id']
        player['first_creative_pos'] = (player['x'], player['y'])
        if player['creative_lines_points']:
            player['creative_lines_points'].clear()

    if player["creating"]:
        creative_actions(player)
    else:
        normal_actions(player)
