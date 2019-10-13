import numpy as np
import random
from collections import deque
from keras.models import clone_model


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
        self.memory = [] #deque(maxlen=1000)

    """ Returns the action with the highest expected reward """
    def act(self, state, allowed_actions):
        if np.random.random() < self.epsilon:
            return np.random.choice(allowed_actions)
        state = np.reshape(state, [1, len(state)])       
        scores = self.model.predict(state)
        max_score = max(np.take(scores[0], allowed_actions))
        best_actions = [a for a in allowed_actions if scores[0][a] == max_score]
        if not best_actions:
            print(state, scores, max_score, best_actions)
        return np.random.choice(best_actions)

    def remember(self, state, reward, action, next_state, done, allowed_actions): 
        state = np.reshape(state, [1, len(state)]) 
        next_state = np.reshape(next_state, [1,  len(next_state)])
        self.memory.append((state, action, reward, next_state, done, allowed_actions))
    
    def inherit(self):
        return Agent(self.model, self.epsilon, self.alpha, self.gamma, self.learning_rate)

    def replay(self, batch_size):
        # size = len(self.memory)
        # for i in range(int(np.ceil(size / batch_size))):
        #     temp_model = clone_model(self.model)
        for state, action, reward, next_state, done, allowed_actions in self.memory:
                # self.memory[i * batch_size: min((i + 1) * batch_size, size)]:
            target = reward + (1 - done) *  self.gamma * np.amax(np.take(self.model.predict(next_state)[0], allowed_actions))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
