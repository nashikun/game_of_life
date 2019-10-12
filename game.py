
import matplotlib.pyplot as plt
import time
from tkinter import *

class Game:
    def __init__(self):
        self.moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt'}  
        self.count = 0  
        self.animation = Tk()
        self.canvas = Canvas(self.animation, width = 400, height = 400)
        self.canvas.pack()
        self.player = Player(self.canvas, self.animation)

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

class Player:
    def __init__(self, canvas, animation):
        self.canvas = canvas
        self.animation = animation
        self.hunger = 0
        self.stamina = 100
        self.set_canvas()

    def set_canvas(self):
        self.hunger_bar = self.canvas.create_rectangle(50, 50, 50, 100, fill='red')
        self.hunger_text = StringVar()
        self.hunger_label = Label(self.animation, textvariable=self.hunger_text)
        self.hunger_label.pack()
        self.stamina_bar = self.canvas.create_rectangle(50, 150, 150, 200, fill='red')
        self.stamina_text = StringVar()
        self.stamina_label = Label(self.animation, textvariable=self.stamina)
        self.stamina_label.pack()

    def draw(self):
        self.canvas.coords(self.hunger_bar, 50, 50, 50 + self.hunger, 100)
        self.canvas.coords(self.stamina_bar, 50, 150, 50 + self.stamina, 200)
        self.hunger_text.set("Hunger: %s / 100 "%self.hunger)
        self.stamina_text.set("Stamina: %s / 100 "%self.stamina)

    def play_turn(self):
        self.hunger += 1

    def is_dead(self):
        return self.stamina <= 0 or self.hunger >= 100

if __name__ == "__main__":
    game = Game()
    game.run()
