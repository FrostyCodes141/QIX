# retrieve saved parameters
saved_parameters = {}
with open("config.txt") as f:
    for line in f:
        line = line.split(':')
        saved_parameters[line[0]] = line[1][:-1]


# constants
all_lines = {}
line_size = 5
all_polygons = []

all_players = []
player_size = 5
player_velocity = int(saved_parameters['player_velocity'])
bonus_speed = 1

all_qix = []
qix_size = 60
qix_speed = 1
max_timer = 100

all_sparx = []
sparx_speed = 1
sparx_size = 5

window_width = int(saved_parameters['window_width'])
window_height = int(saved_parameters['window_height'])
surface_size = int(saved_parameters['surface_size'])
total_surface = surface_size**2

all_obstacles = []
num_obstacles = int(saved_parameters['num_obstacles'])
obstacle_size = 15

all_apples = []
num_apples = int(saved_parameters['num_apples'])
apple_size = 5

all_checkbox = {}
checkbox_size = 50

game = {}
pressed = {'p': False}
