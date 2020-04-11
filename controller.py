from games import Connect4
from interfaces import Connect4WebInterface
from agents import BasicAgent
import time
import threading

game = Connect4()
agent = BasicAgent(game=game)

def alternate_turns():
    while True:

        if game.winner is not None:
            pass

        # player 0 is human on interface
        elif game.player == 0:
            time.sleep(0.1)
        
        # player 1 is agent
        elif game.player == 1:
            agent.make_move()

threading.Thread(target=alternate_turns).start()

interface = Connect4WebInterface(game=game)
