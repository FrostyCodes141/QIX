from database import save_played_game
from fltk import rectangle, touche_pressee, cree_fenetre, ferme_fenetre, efface_tout, mise_a_jour
from game_functions import display_menu, do_updates, init_game_parameters, next_level, enable_checkbox, \
    display_option_menu, save_parameters, display_controls_menu
from constants import window_width, window_height, game, pressed


def main() -> None:
    """ main function """
    cree_fenetre(window_width, window_height)
    init_game_parameters()
    enable_checkbox()
    while True:
        efface_tout()
        rectangle(0, 0, window_width, window_height, remplissage="black")
        if game['is_playing']:
            # if the game is running
            if game['has_win']:
                next_level()
                game['has_win'] = False
            do_updates()
        else:
            # if the game is not running, the menu is displayed
            if game['option_menu']:
                # option menu
                display_option_menu()
            elif game['controls_menu']:
                # controls menu
                display_controls_menu()
            else:
                display_menu()
        mise_a_jour()
        if touche_pressee('Escape'):
            save_parameters()
            break
        if pressed['p'] and not touche_pressee('p'):
            pressed['p'] = False
        if game['is_playing'] and touche_pressee('p') and not pressed['p']:
            pressed['p'] = True
            game['is_paused'] = not game['is_paused']
        if game['is_playing'] and touche_pressee('n'):
            save_played_game()
    ferme_fenetre()


if __name__ == '__main__':
    main()

