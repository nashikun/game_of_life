from Game import Game
from Agent import Agent
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os.path
import keras.models
from keras.layers import Dense, LSTM
from keras.models import Sequential
from keras.optimizers import Adam

# The possible actions
moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt', 3 : 'reproduce'}
states = {0 : 'stamina', 1 : 'hunger', 2 : 'food', 3 : 'until_birth', 4 : 'n_children'}
n_moves = len(moves.keys())
n_states = len(states.keys())

class Trainer:
    def __init__(self, epsilon = 1, gamma = 0.99, alpha = 0.5, learning_rate=0.01):
        # Parameters for the Q learning
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.model = self.build_model()
        # Holds the scores of each played game        
        self.scores = []

    def build_model(self):
        model = Sequential()
        # model.add(LSTM(units = 16, batch_input_shape=(1, 1, n_states) ,stateful=True))
        model.add(Dense(64, input_shape = (n_states,), activation='relu', kernel_initializer='random_uniform'))
        model.add(Dense(16, activation='relu', kernel_initializer='random_uniform'))
        model.add(Dense(n_moves, kernel_initializer='random_uniform'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def load_model(self, filename):
        if os.path.isfile(filename):
            self.model = keras.models.load_model(filename)

    def save_model(self, filename):
        self.model.save(filename)
        
    def train(self, show = True, print_scores = True, n_generations = 100):
        self.n_generations = n_generations
        for i in range(n_generations):
            game = Game(show = show, max_value=30, batch_size=32)
            game.add_player(0)
            game.players[0].set_agent(Agent(self.model, self.epsilon, self.alpha, self.gamma, self.learning_rate))
            game.players[0].age = 20
            score = game.run()
            self.updateEpsilon()
            if print_scores:
                print("Score at the %s-th iteration :  %s"%(i, score))
            else:
                if not i % 50:
                    print("%s-th iterations"%i)
            self.scores.append(score)

    def updateEpsilon(self):
        self.epsilon -= 1/self.n_generations

    def plot_scores(self, window=1):
        n_points = int(np.ceil(self.n_generations/window))
        means = [np.mean(self.scores[window * i : min(self.n_generations, window * (i + 1))]) \
                for i in range(n_points)]
        points = [min(window * i, self.n_generations) for i in range(n_points)]
        plt.plot(points, means)
        plt.waitforbuttonpress()

def run_demo(path):
    trainer = Trainer(epsilon=0)
    trainer.load_model(path)
    trainer.train(show=True, print_scores=True, n_generations=1)

def train_model(path, n_generations=1000, window=50):
    trainer = Trainer(epsilon=1)
    trainer.load_model(path)
    trainer.train(show=False, print_scores=False, n_generations=n_generations)
    trainer.plot_scores(window)
    trainer.save_model(path)

if __name__ == "__main__":
    #run_demo("3")
    train_model("3")