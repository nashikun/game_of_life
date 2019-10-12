import time
from tkinter import *

# TODO: if player is pregnant, stamina is reduced and hunger is higher, so they need to stockpile first!

class Player:
    def __init__(self, game, id = 0):
        self.id = id
        self.hunger = 0
        self.food = 0
        self.stamina = game.max_value
        self.max_value = game.max_value
        self.canvas = game.canvas
        self.age = 0
        self.game = game
        self.reward = 0
        if self.canvas:
            self.set_canvas()

    def set_agent(self, agent):
        self.agent = agent

    def set_canvas(self):
        # Hunger meter
        self.hunger_bar = self.canvas.create_rectangle( 150 * self.id + 50, 50, 150 * self.id + 50, 100, fill='red')
        self.hunger_text = StringVar()
        self.hunger_label = Label(textvariable=self.hunger_text)
        self.hunger_label.pack()

        # Stamina meter
        self.stamina_bar = self.canvas.create_rectangle(150 * self.id + 50, 150, 150 * self.id + 250, 200, fill='red')
        self.stamina_text = StringVar()
        self.stamina_label = Label(textvariable=self.stamina_text)
        self.stamina_label.pack()

        # Amount of remaining food
        self.food_text = StringVar()
        self.food_label = Label(textvariable=self.food_text)
        self.food_label.pack()

    def draw(self):
        self.canvas.coords(self.hunger_bar, 150 * self.id + 50, 50, 150 * self.id + 50 + 100 * self.hunger / self.max_value, 100)
        self.canvas.coords(self.stamina_bar, 150 * self.id + 50, 150, 150 * self.id + 50 + 100 * self.stamina / self.max_value, 200)
        self.hunger_text.set("Hunger: %s / %s "%(self.hunger, self.max_value))
        self.stamina_text.set("Stamina: %s / %s "%(self.stamina, self.max_value))
        self.food_text.set("Remaining food: %s"%self.food)

    def next_turn(self, action):
        if action == 0:
            stamina = min(self.stamina + 3, self.max_value)
            hunger = min(1 + self.hunger, self.max_value)
            food = self.food
        elif action == 1 :
            if self.food:
                stamina = self.stamina
                hunger = max(self.hunger - 3, 0)
                food = max(self.food - 1, 0)
            else:
                stamina = self.stamina
                hunger = self.hunger + 1
                food = self.food
        elif action == 2 :
            food = self.food + 2
            hunger = self.hunger + 2
            stamina = self.stamina - 2
        return stamina, hunger, food

    def play_turn(self):
        if not self.is_dead():
            state = (self.stamina, self.hunger, self.food)
            action = self.agent.act(state)
            next_state = self.next_turn(action)
            done = self.game.is_over()
            reward = self.game.reward(next_state)
            self.stamina, self.hunger, self.food = next_state
            self.age += 1
            self.agent.updateQ(state, reward, action, next_state, done)
            self.reward += reward

    def is_dead(self):
        return self.stamina <= 0 or self.hunger >= self.max_value or self.age >= 1000