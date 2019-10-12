from Player import Player
import time
from tkinter import Tk, Canvas
import pickle

class Game:
    """ This class contains a single game, the players and resources"""
    def __init__(self, show= True, max_value = 100):
        # The possible actions
        self.moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt', 3 : 'reproduce'}
        # Number of turns since the start of the game
        self.count = 0
        # Whether to show the canvas
        self.show = show
        # Max health and stamina value
        self.max_value = max_value
        # Defining the canvas
        if self.show:
            self.animation = Tk()
            self.canvas = Canvas(self.animation, width = 400, height = 300)
            self.canvas.pack()
        else:
            self.canvas = None
        self.players = {}

    def add_player(self, id=0):
        """ Adds a player to the game with the corresponding id. No 2 players can have the same id"""
        player = Player(self, id=id)
        if id in self.players.keys():
            raise Exception(('Id already exists'))
        self.players[id] = player

    def run(self):
        """ Runs the game """
        if self.show:
            self.draw()
        while not self.is_over():
            # Each player plays his turn
            for player in self.players.values():
                player.play_turn()
            # Draw the canvas if needed
            if self.show:
                self.draw()
                time.sleep(0.1)
        if self.show:
            self.animation.destroy()
        # The total score is the sum of the rewards for all players
        return sum([player.reward for player in self.players.values()])

    def reward(self, state):
        """ Returns the corresponding reward for a state"""
        stamina, hunger, food, until_birth = state
        return stamina * (food + 4 * (self.max_value - hunger) )

    def draw(self):
        """ Draw the appropriate elements for each player """
        for player in self.players.values():
            player.draw()
        self.animation.update()

    def is_over(self):
        """ Returns True if the game is over and False otherwise"""
        for player in self.players.values():
            if not player.is_dead():
                return False
        return True

    def player(self, id):
        """ Returns the player with the corresponding id, if any """
        if id in self.players.keys():
            return self.players[id]