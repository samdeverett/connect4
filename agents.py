import numpy as np

class BasicAgent():
    def __init__(self, game):
        self.game = game

    def make_move(self):

        h, w = self.game.board.shape

        y = np.random.choice(np.arange(0, h))
        x = np.random.choice(np.arange(0, w))
        choice = (y, x)
        while not self.game.is_available_position(choice):
            y = np.random.choice(np.arange(0, h))
            x = np.random.choice(np.arange(0, w))
            choice = (y, x)
        
        self.game.make_move(choice)
        self.game.next_turn()

class SammysAgent():
    def __init__(self, game):
        self.game = game

    def make_move(self):

        board = self.game.board

        # analyze board
        # todo

        self.game.make_move(move)
        self.game.next_turn()

