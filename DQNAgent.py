from Agent import Agent
import numpy as np
import random
from collections import deque
from keras.models import clone_model

""" The Class responsible for making decisions """
class DQNAgent(Agent):

    """ Returns the action with the highest expected reward """
    def act(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(range(self.n_moves))
        state = np.reshape(state, [1, self.n_states])       
        scores = self.model.predict(state)
        max_score = max(scores[0])
        best_actions = [a for a in range(self.n_moves) if scores[0][a] == max_score]
        if not best_actions:
            print(state, scores, max_score, best_actions)
        return np.random.choice(best_actions)

    def update(self, state, reward, action, next_state, done):
        # Updates the memory with normalized states
        state = np.array([[state[0]/ self.max_value - 0.5, state[1]/ self.max_value - 0.5,
        state[2]/ self.max_value - 0.5, state[3], state[4]]])

        next_state = np.array([[next_state[0]/ self.max_value - 0.5, next_state[1]/ self.max_value - 0.5,
        next_state[2]/ self.max_value - 0.5, next_state[3], next_state[4]]])

        self.memory.append((state, reward, action, next_state, done))

    def replay(self, batch_size):
        temp_model = clone_model(self.model)
        X = np.zeros((len(self.memory), self.n_states))
        y = np.zeros((len(self.memory), self.n_moves))
        count = 0
        if self.memory:
            for state, reward, action, next_state, done, in self.memory:
                #self.memory[i * batch_size: min((i + 1) * batch_size, size)]:
                X[count] = state
                target = reward + (1 - done) *  self.gamma * np.amax(temp_model.predict(next_state)[0])
                target_f = self.model.predict(state)
                target_f[0][action] = target
                y[count] = target_f
            self.model.fit(X, y, epochs=5, verbose=0)
        self.memory = deque(maxlen=1000)