import sqlite3
from random import choice

from constants import game, all_apples, all_obstacles, all_lines, all_players, all_qix, all_polygons, all_sparx


def save_played_game():
    db = sqlite3.connect('saved_game.db')
    cur = db.cursor()
    save_apples(cur)
    save_creative_lines_points(cur)
    save_game(cur)
    save_lines(cur)
    save_obstacles(cur)
    save_player(cur)
    save_polygons(cur)
    save_qix(cur)
    save_sparx(cur)
    db.commit()
    cur.close()
    db.close()


def load_apples(cur):
    cur.execute("SELECT * FROM apples")
    for apple in cur.fetchall():
        all_apples.append(apple)


def load_player(cur):
    cur.execute("SELECT * FROM player")
    for player in cur.fetchall():
        p1 = not player[-1]
        all_players.append({
            'id': player[0], 'x': player[1], 'y': player[2], 'velocity': player[3], 'creating': player[4],
            'last_direction': player[5], 'first_creative_line_id': player[6], 'first_creative_pos': (player[7], player[8]),
            'missing_lives': player[9], 'creative_lines_points': [], 'is_alive': bool(player[10]),
            'on_drawing_area': bool(player[11]), 'bonus_speed': player[12], 'invincible_timer': player[13],
            'score': player[14], 'wins': player[15], 'creative_touch': "Return" if p1 else "space",
            'touch_mapping': {"Up": "Up" if p1 else "z", "Down": "Down" if p1 else "s", "Left": "Left" if p1 else "q",
                              "Right": "Right" if p1 else "d"},
            'bonus_speed_touch': "m" if p1 else "f",
        })


def load_creative_lines_points(cur):
    cur.execute("SELECT * FROM creative_lines_points")
    for point in cur.fetchall():
        all_players[point[0]]['creative_lines_points'].append((point[1], point[2]))


def load_game(cur):
    cur.execute("SELECT * FROM game")
    game['surface_filled'], game['percentage_filled'], game['line_id'], game['has_win'], game['additional_speed'], game['qix_amount'], game['sparx_amount'] = cur.fetchone()


def load_lines(cur):
    cur.execute("SELECT * FROM lines")
    for line in cur.fetchall():
        a, b = (line[1], line[2]), (line[3], line[4])
        all_lines[line[0]] = {
            'id': line[0], 'a': a, 'b': b, 'forbidden': line[5], 'is_active': line[6],
            'next_line_id': line[7], 'previous_line_id': line[8], "is_horizontal": a[1] == b[1], "is_vertical": a[0] == b[0]
        }


def load_obstacles(cur):
    cur.execute("SELECT * FROM obstacles")
    for obstacle in cur.fetchall():
        all_obstacles.append(obstacle)


def load_polygons(cur):
    cur.execute("SELECT * FROM polygons")
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'brown', 'grey']
    for point in cur.fetchall():
        if point[0] >= len(all_polygons):
            all_polygons.append([])
            game['polygon_colors'].append(choice(colors))
        all_polygons[-1].append([point[1], point[2]])


def load_qix(cur):
    cur.execute("SELECT * FROM qix")
    for qix in cur.fetchall():
        all_qix.append({
            'x1': qix[0], 'y1': qix[1], 'x2': qix[2], 'y2': qix[3], 'speed': qix[4], 'x_change': qix[5],
            'y_change': qix[6], 'timer': qix[7]
        })


def load_sparx(cur):
    cur.execute("SELECT * FROM sparx")
    for sparx in cur.fetchall():
        all_sparx.append({
            'x': sparx[0], 'y': sparx[1], 'speed': sparx[2], 'direction': sparx[3], 'line_id': sparx[4]
        })


def load_played_game():
    db = sqlite3.connect('saved_game.db')
    cur = db.cursor()
    load_apples(cur)
    load_player(cur)
    load_creative_lines_points(cur)
    load_game(cur)
    load_lines(cur)
    load_obstacles(cur)
    load_polygons(cur)
    load_qix(cur)
    load_sparx(cur)
    cur.close()
    db.close()


def save_apples(cursor):
    cursor.execute("DELETE FROM apples")
    for apple in all_apples:
        cursor.execute("INSERT INTO apples VALUES (?, ?)", [apple[0], apple[1]])


def save_creative_lines_points(cursor):
    cursor.execute("DELETE FROM creative_lines_points")
    for player in all_players:
        for point in player['creative_lines_points']:
            cursor.execute("INSERT INTO creative_lines_points VALUES (?, ?, ?)", [player['id'], point[0], point[1]])


def save_game(cursor):
    cursor.execute("DELETE FROM game")
    data_info = [
        game['surface_filled'], game['percentage_filled'], game['line_id'], game['has_win'],
        game['additional_speed'], game['qix_amount'], game['sparx_amount']
    ]
    cursor.execute("INSERT INTO game VALUES (?, ?, ?, ?, ?, ?, ?)", data_info)


def save_lines(cursor):
    cursor.execute("DELETE FROM lines")
    for line in all_lines.values():
        data_info = [
            line['id'], line['a'][0], line['a'][1], line['b'][0], line['b'][1], line['forbidden'], line['is_active'],
            line['next_line_id'], line['previous_line_id']
        ]
        cursor.execute("INSERT INTO lines VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_info)


def save_obstacles(cursor):
    cursor.execute("DELETE FROM obstacles")
    for obstacle in all_obstacles:
        cursor.execute("INSERT INTO obstacles VALUES (?, ?)", [obstacle[0], obstacle[1]])


def save_player(cursor):
    cursor.execute("DELETE FROM player")
    for i, player in enumerate(all_players):
        data_info = [
            player['id'], player['x'], player['y'], player['velocity'], player['creating'], player['last_direction'],
            player['first_creative_line_id'], player['first_creative_pos'][0], player['first_creative_pos'][1],
            player['missing_lives'], player['is_alive'], player['on_drawing_area'], player['bonus_speed'],
            player['invincible_timer'], player['score'], player['wins'], i%2
        ]
        cursor.execute("INSERT INTO player VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data_info)


def save_polygons(cursor):
    cursor.execute("DELETE FROM polygons")
    for i, polygon in enumerate(all_polygons):
        for point in polygon:
            cursor.execute("INSERT INTO polygons VALUES (?, ?, ?)", [i, point[0], point[1]])


def save_qix(cursor):
    cursor.execute("DELETE FROM qix")
    for qix in all_qix:
        data_info = [
            qix['x1'], qix['y1'], qix['x2'], qix['y2'], qix['speed'], qix['x_change'], qix['y_change'], qix['timer']
        ]
        cursor.execute("INSERT INTO qix VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data_info)


def save_sparx(cursor):
    cursor.execute("DELETE FROM sparx")
    for sparx in all_sparx:
        data_info = [
            sparx['x'], sparx['y'], sparx['speed'], sparx['direction'], sparx['line_id']
        ]
        cursor.execute("INSERT INTO sparx VALUES (?, ?, ?, ?, ?)", data_info)
