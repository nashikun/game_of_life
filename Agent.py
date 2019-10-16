from collections import deque

class Agent:
    """ The Class responsible for making decisions """
    def __init__(self, model, epsilon,gamma, alpha = None ):
        # Parameters for the Q learning
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        # The number of turns since the start of the game
        self.count = 0
        if self.__module__ != "NaiveDAgent":
            # Holds memory
            self.memory = deque(maxlen=1000)

    def act(self, state, allowed_actions):
        pass

    def update(self, state, reward, action, next_state, done, allowed_actions):
        pass

    def inherit(self):
        if self.alpha:
            return self.__class__(self.model, self.epsilon, self.gamma, self.alpha)
        else:
            return self.__class__(self.model, self.epsilon, self.gamma)

    def replay(self, batch_size):
        pass