from random import randint

from checking_functions import circle_collision, respawn_player, remove_life
from constants import all_obstacles, all_players, obstacle_size, player_size, num_obstacles, window_width, \
    window_height, surface_size, all_checkbox, checkbox_size, num_apples, apple_size, all_apples


def create_checkbox(name: str, text="", is_checked=True) -> dict:
    """ create a checkbox """
    return {
        'name': name,
        'is_checked': is_checked,
        'text': text
    }


def generate_apples():
    """ generate random positions for the obstacles """
    for i in range(num_apples):
        x_min = window_width // 2 - surface_size // 2 + apple_size
        x_max = window_width // 2 + surface_size // 2 - apple_size
        y_min = window_height // 2 - surface_size // 2 + apple_size
        y_max = window_height // 2 + surface_size // 2 - apple_size
        x = randint(x_min, x_max)
        y = randint(y_min, y_max)
        while any(circle_collision((x, y), obstacle_pos(apple), apple_size, apple_size)
                  for apple in all_apples) or any(circle_collision((x, y), obstacle_pos(obstacle), obstacle_size, obstacle_size)
                  for obstacle in all_obstacles):
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
        all_apples.append((x, y))


def generate_obstacles():
    """ generate random positions for the obstacles """
    for i in range(num_obstacles):
        x_min = window_width // 2 - surface_size // 2 + obstacle_size
        x_max = window_width // 2 + surface_size // 2 - obstacle_size
        y_min = window_height // 2 - surface_size // 2 + obstacle_size
        y_max = window_height // 2 + surface_size // 2 - obstacle_size
        x = randint(x_min, x_max)
        y = randint(y_min, y_max)
        while any(circle_collision((x, y), obstacle_pos(obstacle), obstacle_size, obstacle_size)
                  for obstacle in all_obstacles):
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
        all_obstacles.append((x, y))


def obstacle_pos(obstacle):
    return obstacle[0], obstacle[1]


def update_apples() -> None:
    """ check if the player is touching an apple while he is in creative mode """
    for apple in all_apples:
        for player in all_players:
            if circle_collision(obstacle_pos(apple), (player['x'], player['y']), apple_size, player_size):
                player['invincible_timer'] = 200
                all_apples.remove(apple)


def update_obstacles() -> None:
    """ check if the player is touching an obstacle while he is in creative mode """
    for obstacle in all_obstacles:
        for player in all_players:
            if not player["invincible_timer"] and circle_collision(obstacle_pos(obstacle), (player['x'], player['y']), obstacle_size, player_size):
                respawn_player(player)
                remove_life(player)


def verify_checkbox(xp, py, xa, ya):
    """ verify if the player has checked the checkbox """
    for checkbox in all_checkbox.values():
        xb, yb = xa + checkbox_size, ya + checkbox_size
        if xa <= xp <= xb and ya <= py <= yb:
            checkbox['is_checked'] = not checkbox['is_checked']
        ya += checkbox_size + 10
