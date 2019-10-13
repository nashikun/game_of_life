import numpy as np
import random
from collections import deque


class Agent:
    """ The Class responsible for making decisions """
    def __init__(self, model, epsilon, alpha, gamma, learning_rate):
        # Parameters for the Q learning
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.learning_rate = learning_rate
        # The number of turns since the start of the game
        self.count = 0
        # Remembers the previous actions and results 
        self.memory = deque(maxlen=1000)

    """ Returns the action with the highest expected reward """
    def act(self, state, allowed_actions):
        if np.random.random() < self.epsilon:
            return np.random.choice(allowed_actions)
        state = np.reshape(state, [1, len(state)])       
        probas = self.model.predict(state)
        max_proba = max(np.take(probas[0], allowed_actions))
        max_q_actions = [a for a in allowed_actions if probas[0][a] == max_proba]
        return np.random.choice(max_q_actions)

    # def updateQ(self, state, reward, action, next_state, done, allowed_actions):
    #     """ Update the Q matrix """
    #     self.remember(state, action, reward, next_state, done)
    #     max_next_q = max(self.Q[next_state, a] for a in allowed_actions)
    #     self.Q[state, action] += self.alpha * (reward + self.gamma * max_next_q * (1 - done) - self.Q[state, action])

    def remember(self, state, reward, action, next_state, done): 
        state = np.reshape(state, [1, len(state)]) 
        next_state = np.reshape(next_state, [1, len(next_state)])
        self.memory.append((state, action, reward, next_state, done))
    
    def inherit(self):
        return Agent(self.model, self.epsilon, self.alpha, self.gamma, self.learning_rate)

    def replay(self, batch_size):
        if len(self.memory) > batch_size:
            minibatch = random.sample(self.memory, batch_size)
            for state, action, reward, next_state, done in minibatch:
                target = reward
                if not done:
                    target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
                target_f = self.model.predict(state)
                target_f[0][action] = target
                self.model.fit(state, target_f, epochs=1, verbose=0)
