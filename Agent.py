import numpy as np

class Agent:
    """ The Class responsible for making decisions """
    def __init__(self, Q, n_moves, epsilon, alpha, gamma):
        # Parameters for the Q learning
        self.Q = Q
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        # The number of turns since the start of the game
        self.count = 0

    def act(self, state, allowed_actions):
        """ Returns the action with the highest expected reward """
        if np.random.random() < self.epsilon:
            return np.random.choice(allowed_actions)
        qvals = {a : self.Q[state, a] for a in allowed_actions}
        max_q = max(qvals.values())
        max_q_actions = [a for a in allowed_actions if qvals[a] == max_q]
        return np.random.choice(max_q_actions)

    def updateQ(self, state, reward, action, next_state, done, allowed_actions):
        """ Update the Q matrix """
        max_next_q = max(self.Q[next_state, a] for a in allowed_actions)
        self.Q[state, action] += self.alpha * (reward + self.gamma * max_next_q * (1 - done) - self.Q[state, action])

    