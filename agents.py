import numpy as np
import random

class RandomAgent():
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

class MinimaxAgent():
    def __init__(self, game, ply=1):
        self.game = game
        self.maxDepth = ply

    def evaluationFunc(self, board):
        if self.game.did_win(board == 0):
            return float("-inf")
        elif self.game.did_win(board == 1):
            return float("inf")
        else:
            return 0

    def next_board(self, board, action, player):
        next_board = board.copy()
        next_board[action] = player
        print(next_board)
        return next_board

    def make_move(self):

        board = self.game.board
        print(board)

        def value(board, depth, player):
            if self.game.check_gameover() or (depth == self.maxDepth):
                return self.evaluationFunc(board)
            elif player == 0:
                return minValue(board, depth)
            else:
                return maxValue(board, depth)

        def maxValue(board, depth):
            v = float("-inf")
            possibleActions = [(y, x) for y in range(6) for x in range(7) if board[(y,x)] == -1 and not np.any(board[y+1:, x] == -1)]
            for action in possibleActions:
                successor = self.next_board(board, action, 1)
                v = max(v, value(successor, depth, 0))
            return v

        def minValue(board, depth):
            v = float("inf")
            possibleActions = [(y, x) for y in range(6) for x in range(7) if board[(y,x)] == -1 and not np.any(board[y+1:, x] == -1)]
            print(possibleActions)
            for action in possibleActions:
                successor = self.next_board(board, action, 0)
                print(f'utility = {value(successor, depth + 1, 1)}')
                v = min(v, value(successor, depth + 1, 1))
            return v

        possibleActions = [(y, x) for y in range(6) for x in range(7) if self.game.is_available_position((y, x))]
        actionUtilities = {}
        for action in possibleActions:
            print(f'checking successor for {action}')
            successor = self.next_board(board, action, 1)
            print(f'adding utility for {action}')
            actionUtilities[action] = value(successor, 0, 0)
        print('showing all utilities:')
        print(actionUtilities)
        maxUtility = max(actionUtilities.values())
        bestMoves = []
        for m, v in actionUtilities.items():
            if v == maxUtility:
                bestMoves.append(m)
        move = random.choice(bestMoves)
        print(f'Choosing move {move}')

        # analyze board
        # todo

        self.game.make_move(move)
        self.game.next_turn()
