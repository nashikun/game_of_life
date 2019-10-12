from collections import defaultdict
import numpy as np
Q = defaultdict(float)

class Agent:
    def __init__(self, game, epsilon, alpha, gamma):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.actions = range(len(game.moves.keys()))
        print(len(Q.items()))

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        qvals = {a : Q[state, a] for a in self.actions}
        max_q = max(qvals.values())
        max_q_actions = [a for a in self.actions if qvals[a] == max_q]
        return np.random.choice(max_q_actions)

    def updateQ(self, state, reward, action, next_state, done):
        max_next_q = max(Q[next_state, a] for a in self.actions)
        Q[state, action] += self.alpha * (reward + self.gamma * max_next_q * (1 - done) - Q[state, action])