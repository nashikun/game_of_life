from Game import Game
from Agent import Agent
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

class Trainer:
    def __init__(self, n_generations, show = True, print_scores = True, epsilon = 1, gamma = 0.99, alpha = 0.5, window = 5):
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.n_generations = n_generations
        self.window = window
        self.scores = []
        Q = defaultdict(float)
        for i in range(n_generations):
            game = Game(show = show, max_value=30)
            game.add_player(0)
            game.players[0].set_agent(Agent(Q,3, self.epsilon, self.alpha, self.gamma))
            score = game.run()
            self.updateEpsilon()
            if print_scores:
                print("Score at the %s-th iteration :  %s"%(i, score))
            else:
                if not i % 50:
                    print("%s-th iterations"%i)
            self.scores.append(score)
        self.plot_scores()
        

    def updateEpsilon(self):
        self.epsilon -= 1/self.n_generations

    def plot_scores(self):
        n_points = int(np.ceil(self.n_generations/self.window))
        means = [np.mean(self.scores[self.window * i : min(self.n_generations, self.window * (i + 1))]) \
                for i in range(n_points)]
        plt.plot(range(n_points), means)
        plt.waitforbuttonpress()

if __name__ == "__main__":
    Trainer(1000, show = False, window=10, print_scores = False)