from checking_functions import find_lines_points, point_in_polygon, check_point_in_line, respawn_player, remove_life
from constants import max_timer, all_lines, all_players, window_height, window_width, surface_size, qix_size, qix_speed, game, all_checkbox
from random import choice, randint


def change_qix_direction(qix: dict, type_change=0) -> None:
    """ change the direction of the qix
     if type_change = 0, the direction is changed randomly
     else, the direction is changed to the opposite """
    if type_change:
        if qix['x_change'] == qix_speed:
            qix['x_change'] = -qix_speed
        elif qix['x_change'] == -qix_speed:
            qix['x_change'] = qix_speed
        if qix['y_change'] == -qix_speed:
            qix['y_change'] = qix_speed
        elif qix['y_change'] == qix_speed:
            qix['y_change'] = -qix_speed
    else:
        qix['x_change'] = choice([-qix_speed, 0, qix_speed])
        qix['y_change'] = choice([-qix_speed, 0, qix_speed])
        if not qix['x_change'] and not qix['y_change']:
            change_qix_direction(qix)


def create_qix():
    x_min = window_width // 2 - surface_size // 2
    y_min = window_height // 2 - surface_size // 2
    x1 = randint(x_min, x_min + surface_size - qix_size)
    y1 = randint(y_min, y_min + surface_size - qix_size)
    x2 = x1 + qix_size
    y2 = y1 + qix_size
    if all_checkbox['speed_increase']['is_checked']:
        velocity =  qix_speed + game['additional_speed']//2
    else:
        velocity = qix_speed + 1
    return {
        'x1': x1,
        'x2': x2,
        'y1': y1,
        'y2': y2,
        'speed': velocity,
        'x_change': choice([-qix_speed, 0, qix_speed]),
        'y_change': choice([-qix_speed, 0, qix_speed]),
        'timer': 0
    }


def detect_qix_collision(qix: dict) -> bool:
    """ return True if the qix is touching an active line else False """
    x1 = qix['x1']
    y1 = qix['y1']
    x2 = qix['x2']
    y2 = qix['y2']
    qix_points = find_lines_points(x1, y1, x2, y2)
    return any(
        check_point_in_line(qix_point[0], qix_point[1], line)
        for line in all_lines.values()
        for qix_point in qix_points
    )


def detect_qix_creative_collision(qix: dict, player: dict) -> bool:
    """ return True if the qix is touching a line drawn by the player else False """
    x1 = qix['x1']
    y1 = qix['y1']
    x2 = qix['x2']
    y2 = qix['y2']

    # adding player coordinates to the creative lines points
    tempo_lst = player['creative_lines_points'].copy()
    tempo_lst.append((player['x'], player['y']))

    for i in range(len(tempo_lst)-1):
        a = tempo_lst[i]
        b = tempo_lst[i + 1]

        # a must be the point with the lowest coordinates
        if a[0] > b[0] or a[1] > b[1]:
            a, b = b, a

        all_qix_points = find_lines_points(x1, y1, x2, y2)
        for qix_point in all_qix_points:
            if check_point_in_line(qix_point[0], qix_point[1], {'a': a, 'b': b}):
                return True
    return False


def qix_in_polygon(qix: dict, checked_polygon: list) -> bool:
    """ return True if the qix is in the checked_polygon else False """
    qix_points = find_lines_points(qix['x1'], qix['y1'], qix['x2'], qix['y2'])
    return any(
         point_in_polygon(qix_point[0], qix_point[1], checked_polygon)
         for qix_point in qix_points
    )


def qix_movement(qix: dict) -> None:
    """ make the qix move in his direction """
    qix['x1'] += qix["x_change"]
    qix['x2'] += qix["x_change"]
    qix['y1'] += qix["y_change"]
    qix['y2'] += qix["y_change"]


def update_qix(qix: dict) -> None:
    """ update qix information """
    # update qix position and direction
    qix_movement(qix)

    # if the qix is touching a line, we change his direction
    if detect_qix_collision(qix):
        change_qix_direction(qix, type_change=1)
        while (detect_qix_collision(qix)):
            qix_movement(qix)
    
    update_qix_direction(qix)

    # if the qix is touching a line drawn by the player, we respawn the player and remove a life
    for player in all_players:
        if player['creating'] and detect_qix_creative_collision(qix, player):
            if not player["invincible_timer"]:
                respawn_player(player)
                remove_life(player)
            else:
                change_qix_direction(qix, type_change=1)


def update_qix_direction(qix: dict) -> None:
    """ Update qix direction after a certain time """
    qix['timer'] += 1
    if qix['timer'] == max_timer:
        qix['timer'] = 0
        change_qix_direction(qix)
