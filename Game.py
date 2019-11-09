from Human import Human
from NaiveQAgent import NaiveQAgent
import time
from tkinter import Tk, Canvas
import pickle
import random

class Game:
    """ This class contains a single game, the players and resources"""
    def __init__(self, show= True, max_value = 100, batch_size = 32):
        # Number of turns since the start of the game
        self.count = 0
        # Whether to show the canvas
        self.show = show
        # Max health and stamina value
        self.max_value = max_value
        # The batch size for training the model
        self.batch_size = batch_size
        # Defining the canvas
        if self.show:
            self.animation = Tk()
            self.canvas = Canvas(self.animation, width = 2000, height = 300)
            self.canvas.pack()
        else:
            self.canvas = None
        self.players = {}
        self.new_borns = {}

    def add_player(self, id=None, random_state=False):
        """ Adds a player to the game with the corresponding id. No 2 players can have the same id"""
        if id:
            if id in self.players.keys():
                raise Exception(('Id already exists'))
            the_id = id
        else:
            the_id = max(self.players.keys(), default = -1) + 1
        self.players[the_id] = Human(self, id=the_id)
        if random_state:
            self.players[the_id].stamina = random.randint(0, self.max_value)
            self.players[the_id].hunger = random.randint(0, self.max_value)
    
    def add_new_born(self, parent):
        """ Adds a player as some player's child"""
        # The list of all used ids
        keys = set(self.players.keys()) | set(self.new_borns.keys())
        new_id = max(keys, default = -1) + 1
        player = Human(self, id = new_id, parent = parent)
        player.set_agent(parent.agent.inherit())
        parent.children.append(player)
        # New_borns is a temporary dict holding new born players,
        # since we're iterating over self.players and can't change it at the same time
        self.new_borns[new_id] = player

    def run(self):
        """ Runs the game """
        if self.show:
            self.draw()
        while not self.is_over():
            # Each player plays his turn
            for player in self.players.values():
                player.play_turn()
            self.players = {**self.players, **self.new_borns}
            self.new_borns = {}
            # Draw the canvas if needed
            if self.show:
                self.draw()
                time.sleep(0.1)
        for player in self.players.values():
            player.agent.replay(self.batch_size)
        if self.show:
            self.animation.destroy()
        # The total score is the sum of the rewards for all players
        return self.player(0).reward #sum([player.reward for player in self.players.values()])

    def reward(self, state):
        """ Returns the corresponding reward for a state"""
        stamina, hunger, food, _ , n_children = state
        return min(self.max_value / 2 - hunger, stamina - self.max_value / 2)
        # score = stamina * (food + 4 * (self.max_value - hunger))
        # if n_children : 
        #    score *= 1.5
        # return score

    def draw(self):
        """ Draw the appropriate elements for each player """
        for player in self.players.values():
            player.draw()
        self.animation.update()

    def is_over(self):
        """ Returns True if the game is over and False otherwise"""
        if self.count > 1000:
            return True
        for player in self.players.values():
            if not player.is_dead():
                return False
        return True

    def player(self, id):
        """ Returns the player with the corresponding id, if any """
        if id in self.players.keys():
            return self.players[id]