from random import choice

from constants import all_polygons, all_lines, all_players, all_sparx, game, all_qix
from checking_functions import line_in_greater_line, check_point_in_line, determine_forbidden, polygon_area, add_score, point_in_polygon, respawn_player, remove_life
from fltk import cercle, attend_clic_gauche
from qix import qix_in_polygon


def add_polygons_points(line: dict, actual_line_point: str, first_id: str, second_id: str, player: dict) -> list:
    """ return a polygon created with the points of the creative lines
    actual_line_point : str representing the first point that will be checked to complete the polygon
    first_id : str representing the first neighbor of 'line' that will be checked
    second_id : str representing the second neighbor of 'line' that will be checked if we can't check the first one
    """

    # last_point represent the point where the player enabled creative mode (will be the last point of the polygon)
    last_point = player['creative_lines_points'][0]

    # copying stuff to not modify the original
    actual_polygon = player['creative_lines_points'].copy()
    actual_line = line.copy()

    # represents the extremity we want to check of 'line'
    actual_point = actual_line[actual_line_point]

    # adding points to the polygon while we have not found 'last_point'
    while not check_point_in_line(last_point[0], last_point[1], actual_line):
        # adding the point of the line we have not checked yet in the polygon
        if actual_line['a'] == actual_point:
            actual_polygon.append(actual_line['b'])
            actual_point = actual_line['b']
        else:
            actual_polygon.append(actual_line['a'])
            actual_point = actual_line['a']

        # getting the neighboring lines of 'line'
        next_line1 = all_lines[actual_line[first_id]]
        next_line2 = all_lines[actual_line[second_id]]

        # checking the neighboring line we have not checked yet
        actual_line = next_line1 if actual_point in next_line1.values() else next_line2
    return actual_polygon


def add_surface(line: dict, player: dict) -> None:
    """ adding surface delimited by the player """

    # getting the two polygons that can be created
    next_polygon = add_polygons_points(line, 'a', 'next_line_id', 'previous_line_id', player)
    former_polygon = add_polygons_points(line, 'b', 'previous_line_id', 'next_line_id', player)

    # determine which polygon to draw
    np_count = 0
    fp_count = 0
    for qix in all_qix:
        # adding the polygon that does not contain the qix and updating the score
        if qix_in_polygon(qix, next_polygon):
            np_count += 1
        else:
            fp_count += 1
    
    np_area = polygon_area(next_polygon)
    fp_area = polygon_area(former_polygon)

    if fp_count < np_count:
        add_polygon(former_polygon, fp_area, player)
    elif np_count < fp_count:
        add_polygon(next_polygon, np_area, player)
    else:
        if np_area < fp_area:
            add_polygon(next_polygon, np_area, player)
        else:
            add_polygon(former_polygon, fp_area, player)
    
    # adding a random color for polygons
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'brown', 'grey']
    game['polygon_colors'].append(choice(colors))


def add_polygon(polygon, area, player):
    """ add a new polygon and update the score """
    all_polygons.append(polygon)
    add_score(area, player)
    for player2 in all_players:
        if player2 != player and point_in_polygon(player2['x'], player2['y'], polygon):
            respawn_player(player2)
            remove_life(player2)


def change_line(line_to_change: dict, a: tuple, b: tuple, new_lines_ids: list) -> None:
    """ change information of 'line_to_change' """
    la = line_to_change['a']
    lb = line_to_change['b']

    # disabling the former line (not deleting it because sparx can be on it)
    line_to_change['is_active'] = False

    # creating the new lines
    create_new_lines(a, b, new_lines_ids, la, lb)

    # updating player information
    for player in all_players:
        if player['first_creative_line_id'] == line_to_change['id']:
            if player['creative_lines_points']:
                xp, yp = player['creative_lines_points'][0]
            else:
                xp, yp = player['x'], player['y']
            for line_id in new_lines_ids:
                if check_point_in_line(xp, yp, all_lines[line_id]):
                    player['first_creative_line_id'] = line_id
                    break

    # updating sparx information
    for sparx in all_sparx:
        update_object_line_id(sparx, line_to_change)


def change_neighbor(line: dict, new_neighbor: dict) -> None:
    """ change the neighboring lines of 'line' """
    if line['a'] in (new_neighbor['a'], new_neighbor['b']):
        line['previous_line_id'] = new_neighbor['id']
    elif line['b'] in (new_neighbor['a'], new_neighbor['b']):
        line['next_line_id'] = new_neighbor['id']


def check_line_changing(point: tuple, line: dict, line2: dict, line_to_check: str) -> None:
    """ check if we need to change the neighboring lines of 'line' """
    # checking if there is a common point between 'line' and 'line2', if so we change the neighboring lines
    if point in (line2['a'], line2['b']):
        if line['is_active']:
            change_neighbor(line2, line)
        if line2['is_active'] or not line['is_active']:
            line[line_to_check] = line2['id']


def create_and_pick_line_id(a, b, line_id, is_active=True, n_id=-1, p_id=-1) -> int:
    """ create a new line and return its id """
    if line_id == -1:
        line_id = get_new_line_id()
    all_lines[line_id] = create_line(line_id, a, b, determine_forbidden(a, b), is_active, n_id, p_id)
    return line_id


def create_line(id_line: int, a: tuple, b: tuple, forbidden: str, is_active: bool, next_line_id: int, previous_line_id: int) -> dict:
    """ create new line with his
     'id' : int (id of the line)
     'a' : tuple (x, y) (first point of the line)
     'b' : tuple (x, y) (second point of the line)
     'color' : str (color of the line)
     'forbidden' : str (direction where the player can not go)
     'is_active' : bool (if the player can go on the line)
     'is_horizontal' : bool (if the line is horizontal)
     'is_vertical' : bool (if the line is vertical)
     'next_line_id' : int (id of the next line)
     'previous_line_id' : int (id of the previous line)
    """
    return {
        'id': id_line,
        'a': a,
        'b': b,
        'forbidden': forbidden,
        'is_active': is_active,
        'is_horizontal': a[1] == b[1],
        'is_vertical': a[0] == b[0],
        'next_line_id': next_line_id,
        'previous_line_id': previous_line_id
    }


def create_new_lines(a, b, new_lines_ids, la, lb) -> None:
    """ divides a line into several other lines """
    # if there is space between at the left or at the top of the line, we create a new line
    lid = get_new_line_id()
    if la != a:
        new_lines_ids.append(create_and_pick_line_id(la, a, -1))

    # creating new line in the middle
    bl_id = get_new_line_id()
    new_lines_ids.append(create_and_pick_line_id(a, b, lid, is_active=False))

    # if there is space between at the right or at the bottom of the line, we create a new line
    if b != lb:
        new_lines_ids.append(create_and_pick_line_id(b, lb, bl_id))
        all_lines[new_lines_ids[-2]]['next_line_id'] = new_lines_ids[-1]


def get_new_line_id() -> int:
    """ return a new line id and add it to a list if lst is not None """
    game['line_id'] += 1
    return game['line_id']


def update_line_neighbor(line: dict) -> None:
    """ update the neighboring lines of 'line' """
    for line2 in all_lines.values():
        if line2['id'] != line['id']:
            check_line_changing(line['a'], line, line2, 'previous_line_id')
            check_line_changing(line['b'], line, line2, 'next_line_id')


def update_lines() -> None:
    """ updates all lines information when a new surface is added """
    # getting the last polygon added
    checked_polygon = all_polygons[-1]
    new_lines_ids = []
    poly_size = len(checked_polygon)
    for i in range(poly_size):
        a = checked_polygon[i]
        b = checked_polygon[i + 1] if i + 1 < poly_size else checked_polygon[0]

        # a must be the point with the lowest coordinates
        if a[0] > b[0] or a[1] > b[1]:
            a, b = b, a

        line_to_change = line_in_greater_line(a, b)
        if line_to_change is not None:
            change_line(line_to_change, a, b, new_lines_ids)
            all_lines.pop(line_to_change['id'])
        elif a != b:
            new_lines_ids.append(create_and_pick_line_id(a, b, -1))
    [update_line_neighbor(l) for l in all_lines.values()]


def update_object_line_id(entity, line_to_change, id_text="line_id") -> None:
    """ update the line id of an object """
    # we update the line id of the entity only if he is on the line we are changing
    if entity[id_text] != line_to_change['id']:
        return

    # putting the entity's line_id to the line he is currently on
    for line in all_lines.values():
        if line['id'] != line_to_change['id'] and check_point_in_line(entity['x'], entity['y'], line):
            entity[id_text] = line['id']
            return
