from random import choice

from constants import window_width, window_height, surface_size, all_polygons, all_lines, game, total_surface, \
    all_players
from math import sqrt


def add_score(surface: float, player: dict) -> None:
    """ update score and surface filled """

    coef = 200 if player['bonus_speed'] else 150

    # update score
    player['score'] += round(surface / coef)

    # update surface filled
    game['surface_filled'] += surface
    game['percentage_filled'] = game['surface_filled'] * 100 / total_surface
    if game['percentage_filled'] >= 75:
        game['has_win'] = True


def can_add_surface(player) -> bool:
    """ checking if we can draw a new surface """
    # checking if there is at least one line to draw
    if not player['creative_lines_points']:
        return False

    # adding player coordinates to the creative lines points
    player['creative_lines_points'].append((player['x'], player['y']))

    # will return False if the player has not gone into the drawing area
    x, y = player['creative_lines_points'][1]
    line = all_lines[player['first_creative_line_id']]
    return not check_point_in_line(x, y, line)


def check_entity_on_line(entity: dict, text_line="line_id") -> None:
    """ check if the sparx is still on his line, if not we replace him on his line """
    l = all_lines[entity[text_line]]
    if not check_point_in_line(entity['x'], entity['y'], l):
        a, b = l['a'], l['b']
        if l['is_horizontal']:
            if entity['x'] < a[0]:
                entity['x'] = a[0]
            elif entity['x'] > b[0]:
                entity['x'] = b[0]
        elif l['is_vertical']:
            if entity['y'] < a[1]:
                entity['y'] = a[1]
            elif entity['y'] > b[1]:
                entity['y'] = b[1]


def check_movement_allowed(direction: str, player: dict) -> bool:
    """ checking if the player is allowed to go in a certain direction """
    """    if direction in ("right", "left"):
        all_x = [i for i in range(player['x'] - player['velocity'], player['x'] + player['velocity'] + 1)]
        all_y = [player['y']]
    else:
        all_y = [i for i in range(player['y'] - player['velocity'], player['y'] + player['velocity'] + 1)]
        all_x = [player['x']]"""
    for line in all_lines.values():
        if check_point_in_line(player['x'], player['y'], line) and line['is_active']:
            if line['forbidden'] == direction:
                return False
            break
    return True


def check_player_in_line(line, player):
    xp = player['x']
    yp = player['y']
    xa = line['a'][0]
    ya = line['a'][1]
    xb = line['b'][0]
    yb = line['b'][1]
    if ya > yb or xa > xb:
        xa, xb, ya, yb = xb, xa, yb, ya
    if line['is_horizontal']:
        if xa < xp < xb and ya == yp:
            return True
    elif line['is_vertical']:
        if ya < yp < yb and xa == xp:
            return True
    return False


def check_point_in_line(x: int, y: int, line, player=None) -> bool:
    """ return True if the point (x, y) is in 'line' else False """
    xa, ya = line['a']
    xb, yb = line['b']
    if player is not None:
        if player['last_direction'] == "up":
            yb += player['velocity']
        elif player['last_direction'] == "down":
            ya -= player['velocity']
        elif player['last_direction'] == "left":
            xb += player['velocity']
        elif player['last_direction'] == "right":
            xa -= player['velocity']
    return xa <= x <= xb and ya <= y <= yb


def circle_collision(a: tuple, b: tuple, ra: int, rb: int) -> bool:
    """ return True if the circle 'a' is touching the circle 'b' else False """
    return sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2) < ra + rb


def determine_forbidden(a, b):
    if a[0] == b[0]:
        if invalid_point(a[0]+1, (a[1]+b[1])/2):
            return "Right"
        elif invalid_point(a[0]-1, (a[1]+b[1])/2):
            return "Left"
    elif a[1] == b[1]:
        if invalid_point((a[0]+b[0])/2, a[1]+1):
            return "Down"
        elif invalid_point((a[0]+b[0])/2, a[1]-1):
            return "Up"
    return "None"


def entity_pos(entity):
    return entity['x'], entity['y']


def find_lines_points(x1: int, y1: int, x2: int, y2: int) -> list[tuple[int, int]]:
    """ return all the points of the lines between (x1, y1) and (x2, y2) """
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steps = int(dx) if dx >= dy else int(dy)
    if steps == 0:
        return [(x1, y1)]
    x_step = (x2 - x1) / steps
    y_step = (y2 - y1) / steps
    for i in range(steps + 1):
        x = x1 + i * x_step
        y = y1 + i * y_step
        points.append((int(round(x)), int(round(y))))
    return points


def get_line(xp, yp, check_active=True):
    for line in all_lines.values():
        x1, y1 = line["a"]
        x2, y2 = line["b"]
        if x1 <= xp <= x2 and y1 <= yp <= y2:
            if check_active and not line["is_active"]:
                continue
            return line


def get_line_collision(player) -> dict:
    """ check if the player is on a line """
    for line in all_lines.values():
        if line['is_active'] and check_point_in_line(player['x'], player['y'], line):
            return line
    return {}


def invalid_point(x, y):
    if x > window_width // 2 + surface_size // 2 or x < window_width // 2 - surface_size // 2\
            or y > window_height // 2 + surface_size // 2 or y < window_height // 2 - surface_size // 2:
        return True
    return any(point_in_polygon(x, y, checked_polygon) for checked_polygon in all_polygons)


def line_in_greater_line(a, b):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    for line in all_lines.values():
        xl1 = line['a'][0]
        xl2 = line['b'][0]
        yl1 = line['a'][1]
        yl2 = line['b'][1]
        if xl1 <= x1 <= x2 <= xl2 and yl1 <= y1 <= y2 <= yl2 and line['is_active']:
            return line
    return None


def point_in_active_line(player, x=-1, y=-1) -> bool:
    """ return True if the player is on an active line else False """
    if x == -1 and y == -1:
        x, y = player['x'], player['y']
    return any(
        check_point_in_line(x, y, line) and line['is_active']
        for line in all_lines.values()
    )


def point_in_polygon(x: int, y: int, checked_polygon: list[tuple[int, int]]) -> bool:
    """ return True if the point is in the checked_polygon else False """
    n = len(checked_polygon)
    c = False
    j = n - 1
    for i in range(n):
        xi, yi = checked_polygon[i]
        xj, yj = checked_polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            c = not c
        j = i
    return c


def polygon_area(p: list[int]) -> float:
    """ calculate the area of a polygon """
    return 0.5 * abs(sum(x0 * y1 - x1 * y0
                         for ((x0, y0), (x1, y1)) in zip(p, p[1:] + [p[0]])))


def position_test(pos: str, player) -> int:
    """ return True if the player can go to the direction 'pos' else False """
    v = player['velocity']

    # changing (x, y) to check the point the player want to go
    for i in range(v, 0, -1):
        x, y = player['x'], player['y']
        y += i if pos == "down" else -i if pos == "up" else 0
        x += i if pos == "right" else -i if pos == "left" else 0
        if point_in_active_line(player, x, y):
            return i
    return 0


def remove_life(player) -> None:
    """ remove a life to the player """
    if player['is_alive']:
        player['missing_lives'] -= 1
    if player['missing_lives'] == 0:
        player['is_alive'] = False


def respawn_player(player) -> None:
    """ respawn the player on a random line """
    player['creative_lines_points'].clear()

    # choosing randomly an active line where the player will respawn
    line_to_respawn = choice(list(all_lines.values()))
    while not line_to_respawn['is_active']:
        line_to_respawn = choice(list(all_lines.values()))

    # updating player information
    player['x'] = (line_to_respawn['a'][0] + line_to_respawn['b'][0]) // 2
    player['y'] = (line_to_respawn['a'][1] + line_to_respawn['b'][1]) // 2
    player['actual_line_id'] = line_to_respawn['id']
    player['creating'] = False
    player['on_drawing_area'] = False
    player['bonus_speed'] = 0


def test_pos(x, y, i, j):
    operations = [(i, 0), (-i, 0), (0, j), (0, -j)]
    for l, c in operations:
        if get_line(x+l, y+c) is not None:
            return l, c

