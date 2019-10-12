import time
from tkinter import *
from Agent import Agent

class Player:
    def __init__(self, id, game):
        self.id = id
        self.agent = Agent(game, 1)
        self.canvas = game.canvas
        self.hunger = 0
        self.food = 0
        self.stamina = 100
        self.set_canvas()

    def set_canvas(self):
        # Hunger meter
        self.hunger_bar = self.canvas.create_rectangle(50, 50, 50, 100, fill='red')
        self.hunger_text = StringVar()
        self.hunger_label = Label(textvariable=self.hunger_text)
        self.hunger_label.pack()

        # Stamina meter
        self.stamina_bar = self.canvas.create_rectangle(50, 150, 250, 200, fill='red')
        self.stamina_text = StringVar()
        self.stamina_label = Label(textvariable=self.stamina_text)
        self.stamina_label.pack()

        # Amount of remaining food
        self.food_text = StringVar()
        self.food_label = Label(textvariable=self.food_text)
        self.food_label.pack()

    def draw(self):
        self.canvas.coords(self.hunger_bar, 50, 50, 50 + 2 *self.hunger, 100)
        self.canvas.coords(self.stamina_bar, 50, 150, 50 + 2 * self.stamina, 200)
        self.hunger_text.set("Hunger: %s / 100 "%self.hunger)
        self.stamina_text.set("Stamina: %s / 100 "%self.stamina)
        self.food_text.set("Remaining food: %s"%self.food)

    def play_turn(self):
        action = self.agent.act([self.stamina, self.hunger])
        if action == 0:
            self.stamina = min(self.stamina + 3, 100)
            self.hunger += 1
        elif action == 1 :
            if self.food:
                self.hunger = max(self.hunger - 3, 0)
                self.food -= 1
            else:
                self.hunger += 1
        elif action == 2 :
            self.food += 2
            self.hunger += 2
            self.stamina -= 2

    def is_dead(self):
        return self.stamina <= 0 or self.hunger >= 100