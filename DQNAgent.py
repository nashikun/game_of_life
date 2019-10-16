from Agent import Agent
import numpy as np
import random
from collections import deque
from keras.models import clone_model

""" The Class responsible for making decisions """
class DQNAgent(Agent):

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

    def update(self, state, reward, action, next_state, done, allowed_actions):
        # Updates the memory
        state = np.reshape(state, [1, len(state)]) 
        next_state = np.reshape(next_state, [1,  len(next_state)])
        self.memory.append((state, reward, action, next_state, done, allowed_actions))

    def replay(self, batch_size):
        temp_model = clone_model(self.model)
        for state, reward, action, next_state, done, allowed_actions in self.memory:
            #self.memory[i * batch_size: min((i + 1) * batch_size, size)]:

            target = reward + (1 - done) *  self.gamma * np.amax(np.take(temp_model.predict(next_state)[0], allowed_actions))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        self.memory = deque(maxlen=1000)