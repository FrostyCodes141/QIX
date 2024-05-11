from checking_functions import check_point_in_line, check_entity_on_line, circle_collision, entity_pos, respawn_player, \
    remove_life
from constants import all_lines, all_players, sparx_size, player_size, sparx_speed, game, all_checkbox


def choose_sparx_direction(sparx, l):
    x, y = entity_pos(sparx)
    h = l['is_horizontal']
    if (x, y) in (l['a'], l['b']):
        a, b = l['a'], l['b']
        sparx['line_id'] = l['id']
        a_point = a[0] if h else a[1]
        s_point = x if h else y

        if s_point == a_point:
            sparx['direction'] = "right" if h else "down"
        else:
            sparx['direction'] = "left" if h else "up"

def create_sparx(x, y, direction, line_id):
    if all_checkbox['speed_increase']['is_checked']:
        velocity =  sparx_speed + game['additional_speed']//2
    else:
        velocity = sparx_speed + 2
    return {
        'x' : x,
        'y' : y,
        'speed' : velocity,
        'direction' : direction,
        'line_id' : line_id
    }


def sparx_test(sparx: dict, direction: str) -> bool:
    x, y = sparx['x'], sparx['y']
    l = all_lines[sparx['line_id']]

    # changing (x, y) to check the point the sparx want to go
    y += 1 if direction == "down" else -1 if direction == "up" else 0
    x += 1 if direction == "right" else -1 if direction == "left" else 0
    # if the sparx is in his line
    if check_point_in_line(x, y, l):
        return True

    # changing sparx direction and line if he is not in his line
    update_sparx_direction(sparx)
    return False


def update_sparx(sparx) -> None:
    """ update sparx information """
    # update sparx position and direction
    update_sparx_movement(sparx)

    # due to his velocity, the sparx can go through a line, so we check if he is still on his line
    check_entity_on_line(sparx)

    # if the sparx is touching the player, the player loses a life and respawns
    for player in all_players:
        if not player["invincible_timer"] and circle_collision(entity_pos(sparx), (player['x'], player['y']), sparx_size, player_size):
            respawn_player(player)
            remove_life(player)


def update_sparx_direction(sparx: dict) -> None:
    l = all_lines[sparx['line_id']]

    pl = all_lines[l['previous_line_id']]
    nl = all_lines[l['next_line_id']]

    choose_sparx_direction(sparx, pl)
    if l == all_lines[sparx['line_id']]:
        choose_sparx_direction(sparx, nl)


def update_sparx_movement(sparx: dict) -> None:
    """ Updates sparx movement based on his axis """
    direction = sparx['direction']
    if direction == "up" and sparx_test(sparx, "up"):
        sparx['y'] -= sparx['speed']
    elif direction == "down" and sparx_test(sparx, "down"):
        sparx['y'] += sparx['speed']
    elif direction == "left" and sparx_test(sparx, "left"):
        sparx['x'] -= sparx['speed']
    elif direction == "right" and sparx_test(sparx, "right"):
        sparx['x'] += sparx['speed']
