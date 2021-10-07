import PySimpleGUI as sg
import sys
sys.path.append(".")
from game_classes import Game

class Game_window(object):
    def Start_screen(self):
        sg.theme('DarkAmber')   # Add a touch of color
        # All the stuff inside your window.
        layout = [  [sg.Text('Player number:')],
                    [sg.Button('1'), sg.Button('2')],
                    [sg.Button('3'),sg.Button('4')],
                    [sg.Button('Cancel')] ]

        # Create the Window
        window = sg.Window('Dominion', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            self.game = Game(int(event))
            break

        window.close()

Gw = Game_window()
Gw.Start_screen()
for i in range(4):
    print(Gw.game.players[str(i)].hand.show())