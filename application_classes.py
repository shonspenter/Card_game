#File that includes the classes that are needed to run the application, not neccesarily the game itself

import sys
sys.path.append(".")
from UI_try import Game_window

class Starting_screen(object):
    def __init__(self):
        Game_window.Start_screen()