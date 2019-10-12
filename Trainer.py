from Game import Game
from Agent import Agent
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pickle

class Trainer:
    def __init__(self, epsilon = 1, gamma = 0.99, alpha = 0.5):
        # Parameters for the Q learning
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        # Holds the Q matrix
        self.Q = defaultdict(float)
        # Holds the scores of each played game        
        self.scores = []



    def load_model(self, path):
        with open(path, 'rb') as handle:
            self.Q = pickle.load(handle)

    def save_model(self, path):
        with open(path, 'wb') as handle:
            pickle.dump(self.Q, handle)
        
    def train(self, show = True, print_scores = True, n_generations = 100):
        self.n_generations = n_generations
        for i in range(n_generations):
            game = Game(show = show, max_value=30)
            game.add_player(0)
            game.players[0].set_agent(Agent(self.Q, self.epsilon, self.alpha, self.gamma))
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
        self.epsilon *= (self.n_generations - 1)/self.n_generations

    def plot_scores(self, window=1):
        n_points = int(np.ceil(self.n_generations/window))
        means = [np.mean(self.scores[window * i : min(self.n_generations, window * (i + 1))]) \
                for i in range(n_points)]
        plt.plot(range(n_points), means)
        plt.waitforbuttonpress()

if __name__ == "__main__":
    trainer = Trainer(epsilon=0.5)
    trainer.load_model("Q_matrix_preg")
    trainer.train(show=True, print_scores=True, n_generations=1)
    #trainer.plot_scores(5)
    #trainer.save_model("Q_matrix_preg")
