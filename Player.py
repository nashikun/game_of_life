import time
from tkinter import *

# TODO: if player is pregnant, stamina is reduced and hunger is higher, so they need to stockpile first!
# TODO : Deque for food to add 'spoiling' 

class Player:
    """ The class for players"""
    def __init__(self, game, id = 0, parent = None):
        # The player's id
        self.id = id
        # Sets the player's parent and children
        self.parent = parent
        self.children = []
        # The player's hunger. They die if it reaches the maximum
        self.hunger = 0
        # The amount of food available for player to eat
        self.food = 0
        # The player's stamina. Used for actions and recovered upon rest
        self.stamina = game.max_value
        # The maximum value for stamina and hunger
        self.max_value = game.max_value
        # The player's age
        self.age = 0
        # Number of turns untill the player gives birth if pregnant 
        self.until_birth = 0
        # The total reward for the player
        self.reward = 0
        # Reference to the played game
        self.game = game
        # Sets up the canvas if needed
        self.canvas = game.canvas
        if game.canvas:
            self.set_canvas()

    def set_agent(self, agent):
        """ Sets an appropriate agent for the player"""
        self.agent = agent

    def set_canvas(self):
        """ Set up the canvas with the appropriate items""" 

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

        # Time till birth
        self.birth_text = StringVar()
        self.birth_label = Label(textvariable=self.birth_text)
        self.birth_label.pack()

    def draw(self):
        """ Draw the player's attributes on the canvas"""
        self.canvas.coords(self.hunger_bar, 150 * self.id + 50, 50, 150 * self.id + 50 + 100 * self.hunger / self.max_value, 100)
        self.canvas.coords(self.stamina_bar, 150 * self.id + 50, 150, 150 * self.id + 50 + 100 * self.stamina / self.max_value, 200)
        self.hunger_text.set("Hunger: %s / %s "%(self.hunger, self.max_value))
        self.stamina_text.set("Stamina: %s / %s "%(self.stamina, self.max_value))
        self.food_text.set("Remaining food: %s"%self.food)
        preg = bool(self.until_birth)
        self.birth_text.set("Is " + "not" * (not preg) + " pregnant." + preg * (" Time till giving birth: %s"%self.until_birth))

    def next_turn(self, action):
        """ Return the next state of player if he did the action in this turn """
        return self.stamina, self.hunger, self.food, self.until_birth, self.n_children()

    def play_turn(self):
        """ Plays 1 turn for the player and updates his status accordingly"""
        if not self.is_dead():
            # The number of alive children
            n_children = self.n_children()
            # If birth is due this turn, give birth
            if self.until_birth == 1:
                self.game.add_new_born(self)
            # The current state
            state = (self.stamina, self.hunger, self.food, self.until_birth, n_children)
            # The best expected action
            action = self.agent.act(state)
            # Do the action
            next_state = self.next_turn(action)
            done = self.game.is_over()
            reward = self.game.reward(next_state)
            # Update the game state
            self.agent.update(state, reward, action, next_state, done)
            self.stamina, self.hunger, self.food, self.until_birth, _ = next_state
            self.age += 1
            self.reward += reward

    def is_dead(self):
        """ Return True if the player is dead and False otherwise"""
        return False

    def n_children(self):
        return len([child for child in self.children if not child.is_dead()])
        