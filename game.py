from Player import Player
import time
from tkinter import Tk, Canvas

class Game:
    def __init__(self):
        self.moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt'}
        self.count = 0
        self.animation = Tk()
        self.canvas = Canvas(self.animation, width = 400, height = 300)
        self.canvas.pack()
        self.player = Player(0, self)

    def run(self):
        self.draw()
        while not self.is_over():
            self.player.play_turn()
            self.draw()
            # self.count += 1
            time.sleep(0.1)


    def draw(self):
        self.player.draw()
        self.animation.update()

    def is_over(self):
        return self.count >= 30 or self.player.is_dead()

if __name__ == "__main__":
    game = Game()
    game.run()
