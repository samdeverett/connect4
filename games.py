import numpy as np

class Connect4():

    def __init__(self):

        # Parameters
        self.dim = 6, 7

        # Runtime variables
        self.board = (np.zeros(self.dim) - 1).astype(int)
        self.turn = 0
        self.player = None
        self.winner = None
        self.next_turn()

    def next_turn(self):
        self.player = self.turn % 2
        self.turn_played = False

    def make_move(self, pos):
        """Run one move by self.player at position pos
        """
        # Can't make move if game over
        if self.winner is not None:
            return

        # Can't make two moves in one turn
        if self.turn_played:
            return

        # Player clicking filled slot does nothing
        if self.board[pos] != -1:
            return

        is_bottom = pos[0] == self.dim[0] - 1
        # Player clicking non-bottom slot does nothing
        if not is_bottom and np.any(self.board[pos[0]+1:, pos[1]] == -1):
            return

        self.board[pos] = self.player
        self.turn_played = True
        self.check_gameover()
        self.turn += 1

    def is_available_position(self, pos):
        is_open = self.board[pos] == -1
        empty_below = np.any(self.board[pos[0]+1:, pos[1]] == -1)

        return is_open and (not empty_below)

    def check_gameover(self):
        for plyr in [0, 1]:
            if self.did_win(self.board == plyr):
                self.winner = plyr
                return True
        # Need a case for tie

    def reset(self):
        self.board = (np.zeros(self.dim) - 1).astype(int)
        self.turn = 0
        self.player = None
        self.winner = None
        self.next_turn()

    def did_win(self, grid):

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
