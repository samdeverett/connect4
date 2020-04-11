##

import random
import numpy as np
import remi.gui as gui
from remi import start, App

class MyApp(App):

    def __init__(self, *args):
        super(MyApp, self).__init__(*args)
        self.turn = 0    # Used to track whose turn it is

    def main(self):

        width, height = 800, 600    # Set board width and height

        svg = gui.Svg(width=width, height=height)
        self.dim = 6, 7    # Set board dimensions
        r = 35    # Set radius of slots
        ys = np.round(np.linspace(2*r, height-2*r, self.dim[0])).astype(int)
        xs = np.round(np.linspace(2*r, width-2*r, self.dim[1])).astype(int)
        self.status = np.zeros(self.dim) - 1
        for rowi, y in enumerate(ys):
            for coli, x in enumerate(xs):
                circ = gui.SvgCircle(x=x, y=y, radius=r)    # Create slot
                circ.style['stroke'] = 'black'    # Set color of slot outline
                circ.style['fill'] = 'white'    # Set color of empty slot
                circ.onclick.do(self.on_click, pos=(rowi, coli))
                svg.append(circ)    # Add slot to GUI

        self.text = gui.Label('')

        container = gui.VBox(width=width, height=height)
        container.append(svg)
        container.append(self.text)
        return container

    def on_click(self, circ, pos=None):

        # player = self.turn % 2

        # Player clicking filled slot does nothing
        if self.status[pos] != -1:
            return

        is_bottom = pos[0] == self.dim[0] - 1
        # Player clicking non-bottom slot does nothing
        if not is_bottom and np.any(self.status[pos[0]+1:, pos[1]] == -1):
            return

        # self.status[pos] = player
        self.status[pos] = 0
        #
        # color = ['black', 'red'][player]
        # circ.style['fill'] = color
        circ.style['fill'] = 'black'

        self.playCPU()

        for plyr in [0, 1]:
            if self.didWin(self.status == plyr):
                # self.text.set_text(f'{color} won!')
                self.text.set_text('Game Over!')

        self.turn += 1

    def playCPU(self):
        pos = random.choice(range(6)), random.choice(range(7))

        is_bottom = pos[0] == self.dim[0] - 1
        # Player clicking non-bottom slot does nothing
        if not is_bottom and np.any(self.status[pos[0]+1:, pos[1]] == -1):
            return

        self.status[pos] = 1
        circ.style['fill'] = 'red'

    def didWin(self, grid):

        def get_depth(pos, grid, covered=None, steps=None):
            pos = np.array(pos)

            if covered is None:
                covered = np.zeros_like(grid)
            covered[tuple(pos)] = 1

            total = 1
            for step in steps:
                new = tuple(pos + step)

                if new[0] < 0 or new[0] >= grid.shape[0]:
                    continue
                if new[1] < 0 or new[1] >= grid.shape[1]:
                    continue

                if covered[new]:
                    continue
                else:
                    covered[new] = 1

                if not grid[new]:
                    continue

                total += get_depth(new, grid, covered, steps)

            return total


        for rowi, row in enumerate(grid):
            for coli, val in enumerate(row):
                if val:
                    for step in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        steps = [np.array(step) * i for i in [1, -1]]
                        if get_depth((rowi, coli), grid, steps=steps) >= 4:
                            return True

        return False


# starts the web server
start(MyApp)

##
