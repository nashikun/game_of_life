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
        if action == 0: # Rest
            if self.until_birth:
                stamina = min(self.stamina + 2, self.max_value)
                hunger = min(2 + self.hunger, self.max_value)
                food = self.food
                until_birth = max(self.until_birth - 1, 0)
            else:
                stamina = min(self.stamina + 4, self.max_value)
                hunger = min(1 + self.hunger, self.max_value)
                food = self.food
                until_birth = max(self.until_birth - 1, 0)
        elif action == 1 : #Eat
            if self.until_birth:
                stamina = self.stamina
                hunger = max(self.hunger - 3, 0)
                food = max(self.food - 2, 0)
                until_birth = max(self.until_birth - 1, 0)
            else:
                stamina = self.stamina
                hunger = max(self.hunger - 3, 0)
                food = max(self.food - 1, 0)
                until_birth = max(self.until_birth - 1, 0)
        elif action == 2 : # Hunt
            if self.until_birth:
                food = self.food + 2
                hunger = self.hunger + 3
                stamina = self.stamina - 4
                until_birth = max(self.until_birth - 1, 0)
            else:
                food = self.food + 2
                hunger = self.hunger + 2
                stamina = self.stamina - 2
                until_birth = max(self.until_birth - 1, 0)
        elif action == 3: # Reproduce
            if self.until_birth:
                raise Exception("Unallowed action")
            else: 
                stamina = self.stamina
                hunger = self.hunger + 2
                food = self.food
                until_birth = 10
        n_children = self.n_children
        return stamina, hunger, food, until_birth

    def play_turn(self):
        """ Plays 1 turn for the player and updates his status accordingly"""
        if not self.is_dead():
            # The allowed actions:
            allowed_actions = self.allowed_actions()
            # The number of alive children
            n_children = self.n_children()
            # If birth is due this turn, give birth
            if self.until_birth == 1:
                self.game.add_new_born(self)
            # The current state
            state = [self.stamina, self.hunger, self.food, self.until_birth]
            # The best expected action
            action = self.agent.act(state, allowed_actions)
            # Do the action
            next_state = self.next_turn(action)
            done = self.game.is_over()
            reward = self.game.reward(next_state)
            # Update the game state
            self.agent.remember(state, reward, action, next_state, done)
            self.stamina, self.hunger, self.food, self.until_birth = next_state
            self.age += 1
            self.reward += reward

    def is_dead(self):
        """ Return True if the player is dead and False otherwise"""
        return self.stamina <= 0 or self.hunger >= self.max_value or self.age >= 100

    def allowed_actions(self):
        """ Returns the list of allowed moves the user can do """
        allowed = [0]
        if self.food : 
            allowed.append(1)
        if self.age > 20:
            allowed.append(2)
            # if not self.until_birth :
            #     allowed.append(3)
        return allowed

    def n_children(self):
        return len([child for child in self.children if not child.is_dead()])
        