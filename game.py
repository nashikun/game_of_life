from Player import Player
import time
from tkinter import Tk, Canvas

class Game:
    def __init__(self, show= True, max_value = 100):
        self.moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt'}
        self.count = 0
        self.show = show
        self.max_value = max_value
        if self.show:
            self.animation = Tk()
            self.canvas = Canvas(self.animation, width = 400, height = 300)
            self.canvas.pack()
        else:
            self.canvas = None
        self.player = Player(self, max_value = max_value)

    def run(self):
        self.draw()
        while not self.is_over():
            self.player.play_turn()
            self.draw()
            time.sleep(0.1)
        if self.show:
            self.canvas.destroy()
        return self.player.reward

    def reward(self, state):
        stamina, hunger, food = state
        return stamina * (food + 4 * (self.max_value - hunger) )

    def draw(self):
        if self.show:
            self.player.draw()
            self.animation.update()

    def is_over(self):
        return self.count >= 30 or self.player.is_dead()

if __name__ == "__main__":
    scores = []
    for i in range(10):
        game = Game(show = False, max_value=10)
        score = game.run()
        print("Score at the %s-th iteration :  %s"%(i, score))
        scores.append(score)
