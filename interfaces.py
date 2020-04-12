import numpy as np
import remi.gui as gui
from remi import start, App
from remi.server import Server
import threading
import time

class Connect4WebInterface():
    def __init__(self, *args, game=None, **kwargs):
        userdata = (game,)
        start(Connect4WebInterface_, *args, userdata=userdata, **kwargs)

class Connect4WebInterface_(App):

    def __init__(self, *args):
        super(Connect4WebInterface_, self).__init__(*args)


    def main(self, game):
        self.game = game
        self.last_known_turn = self.game.turn

        width, height = 800, 600    # Set board width and height

        svg = gui.Svg(width=width, height=height)
        svg.style['background-color'] = 'yellow'
        r = 35    # Set radius of slots
        ys = np.round(np.linspace(2*r, height-2*r, self.game.dim[0])).astype(int)
        xs = np.round(np.linspace(2*r, width-2*r, self.game.dim[1])).astype(int)
        self.grid = np.empty(self.game.dim, dtype='object')
        for rowi, y in enumerate(ys):
            for coli, x in enumerate(xs):
                circ = gui.SvgCircle(x=x, y=y, radius=r)    # Create slot
                circ.style['stroke'] = 'black'    # Set color of slot outline
                circ.style['fill'] = 'white'    # Set color of empty slot
                circ.onclick.do(self.on_click, pos=(rowi, coli))
                svg.append(circ)    # Add slot to GUI
                self.grid[rowi, coli] = circ

        self.text = gui.Label('')
        self.reset_button = gui.Button('Reset Game')
        self.reset_button.onclick.connect(self.reset)

        self.ended = False
        threading.Thread(target=self.update_thread).start()

        container = gui.VBox(width=width, height=height)
        container.append(svg)
        container.append(self.text)
        container.append(self.reset_button)
        return container

    def reset(self, *args, **kwargs):
        self.game.reset()
        self.update_board()
        self.text.set_text('')

    def on_close(self):
        self.ended = True
        super(Connect4WebInterface_, self).on_close()

    def update_thread(self):
        while not self.ended:
            if self.last_known_turn != self.game.turn:
                self.update_board()
                self.last_known_turn = self.game.turn
            time.sleep(0.1)

    def on_click(self, circ, pos=None):
        self.game.make_move(pos)
        self.update_board()
        if self.game.winner is not None:
            self.text.set_text('GAME OVER')
        self.game.next_turn()

    def update_board(self):

        for data, circ in zip(self.game.board.ravel(), self.grid.ravel()):
            if data == -1:
                circ.style['fill'] = 'white'
                continue
            color = ['black', 'red'][data]
            circ.style['fill'] = color
