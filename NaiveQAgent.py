from Agent import Agent
import numpy as np

class NaiveQAgent(Agent):

    """ Returns the action with the highest expected reward """
    def act(self, state, allowed_actions):
        if np.random.random() < self.epsilon:
            return np.random.choice(allowed_actions)
        qvals = {a : self.model[state, a] for a in allowed_actions}
        max_q = max(qvals.values())
        max_q_actions = [a for a in allowed_actions if qvals[a] == max_q]
        return np.random.choice(max_q_actions)

    """ Update the Q matrix """
    def update(self, state, reward, action, next_state, done, allowed_actions):
        max_next_q = max(self.model[next_state, a] for a in allowed_actions)
        self.model[state, action] += self.alpha * (reward + self.gamma * max_next_q * (1 - done) - self.model[state, action])