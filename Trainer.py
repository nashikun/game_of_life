from Game import Game
from NaiveQAgent import NaiveQAgent
from DQNAgent import DQNAgent
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pickle
import keras.models
from keras.layers import Dense, LSTM, Activation, BatchNormalization
from keras.models import Sequential
from keras.optimizers import Adam
from collections import defaultdict

# The possible actions
moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt'} #, 3 : 'reproduce'}
stats = {0 : 'stamina', 1 : 'hunger', 2 : 'food', 3 : 'until_birth', 4 : 'n_children'}
n_moves = len(moves.keys())
n_states = len(stats.keys())

class Trainer:
    def __init__(self, epsilon = 1, gamma = 0.99, alpha = 0.5, learning_rate=0.01, mode = "naive"):
        # Parameters for the Q learning
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.mode = mode
        if mode == "dqn":
            self.model = self.build_model()
        elif mode == "naive":
            self.model = defaultdict(float)
        # Holds the scores of each played game        
        self.scores = []

    def build_model(self):
        model = Sequential()
        # model.add(LSTM(units = 16, batch_input_shape=(1, 1, n_states) ,stateful=True))
        model.add(Dense(15, input_shape = (n_states,), kernel_initializer='random_uniform'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dense(8, kernel_initializer='glorot_uniform'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dense(4, kernel_initializer='glorot_uniform'))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dense(n_moves, kernel_initializer='glorot_uniform'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def load_model(self, filename):
        if os.path.isfile(filename):
            if self.mode == "naive":
                with open(filename, 'rb') as handle:
                    self.model = pickle.load(handle)
            elif self.mode == "dqn":
                self.model = keras.models.load_model(filename)

    def save_model(self, filename):
        if self.mode == "naive":
                with open(filename, 'wb') as handle:
                    pickle.dump(self.model, handle)
        elif self.mode == "dqn":
            self.model.save(filename)
        
    def train(self, show = True, print_scores = True, n_generations = 100, update_epsilon = True, model_path ='', random_state=False, max_value = 30):
        self.n_generations = n_generations
        for i in range(1, n_generations + 1):
            game = Game(show = show, max_value=max_value, batch_size=16)
            game.add_player(0, random_state=random_state)
            if self.mode == "naive":
                agent = NaiveQAgent(n_moves, n_states, self.model, self.epsilon, self.alpha, self.gamma)
            elif self.mode == "dqn":
                agent = DQNAgent(n_moves, n_states, self.model, self.epsilon, self.alpha, self.gamma)
            else:
                print("Invalide mode")
                return
            agent.max_value = max_value
            game.players[0].set_agent(agent)
            game.players[0].age = 20
            score = game.run()
            if update_epsilon:
                self.updateEpsilon()
            if print_scores:
                print("Score at the %s-th iteration :  %s"%(i, score))
            else:
                if not i % 50:
                    print("%s-th iterations"%i)
            if model_path and not i%50:
                self.save_model(model_path)
            self.scores.append(score)
    # Add a policy class. Greedy, epsilon greedy, constant, linear
    def updateEpsilon(self):
        self.epsilon -= 1/self.n_generations

    def plot_scores(self, window=1):
        n_points = int(np.ceil(self.n_generations/window))
        means = [np.mean(self.scores[window * i : min(self.n_generations, window * (i + 1))]) \
                for i in range(n_points)]
        points = [min(window * i, self.n_generations) for i in range(n_points)]
        plt.plot(points, means)
        plt.waitforbuttonpress()

def run_demo(path, random_state = False):
    ext = path.split(".")[-1]
    if ext == "h5":
        mode = "dqn"
    elif ext == "q":
        mode = "naive"
    trainer = Trainer(epsilon=0, mode = mode)
    trainer.load_model(path)
    trainer.train(show=True, print_scores=True, n_generations=1, random_state=random_state)

def train_model(model_path, epsilon=1, n_generations=1000, window=50, read = True, update_epsilon = True, mode = "naive", random_state=False):
    trainer = Trainer(epsilon=epsilon, mode = mode)
    if read:
        trainer.load_model(model_path)
        print("Model loaded")
    trainer.train(show=False, print_scores=False, n_generations=n_generations, update_epsilon=update_epsilon, model_path=model_path, random_state=random_state)
    trainer.plot_scores(window)

if __name__ == "__main__":
   train_model("test.h5", epsilon = 1, read = False, update_epsilon = True, n_generations=1000, window = 50, mode = "dqn", random_state = False)
   #run_demo("attempt.h5", random_state = False)