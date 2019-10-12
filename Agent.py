import numpy as np

class Agent:
    def __init__(self, game, epsilon):
        self.epsilon = epsilon
        self.actions = range(len(game.moves.keys()))

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        