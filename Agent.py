import numpy as np

class Agent:
    def __init__(self, Q, n_moves, epsilon, alpha, gamma):
        self.Q = Q
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.count = 0
        self.actions = range(n_moves)

    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        qvals = {a : self.Q[state, a] for a in self.actions}
        max_q = max(qvals.values())
        max_q_actions = [a for a in self.actions if qvals[a] == max_q]
        return np.random.choice(max_q_actions)

    def updateQ(self, state, reward, action, next_state, done):
        max_next_q = max(self.Q[next_state, a] for a in self.actions)
        self.Q[state, action] += self.alpha * (reward + self.gamma * max_next_q * (1 - done) - self.Q[state, action])

    