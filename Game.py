from Player import Player
import time
from tkinter import Tk, Canvas
import pickle

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
        self.players = {}

    def add_player(self, id=0):
        player = Player(self, id=id)
        if id in self.players.keys():
            raise Exception(('Id already exists'))
        self.players[id] = player

    def run(self):
        if self.show:
            self.draw()
        while not self.is_over():
            for player in self.players.values():
                player.play_turn()
            if self.show:
                self.draw()
                time.sleep(0.1)
        if self.show:
            self.animation.destroy()
        return sum([player.reward for player in self.players.values()])

    def reward(self, state):
        stamina, hunger, food = state
        return stamina * (food + 4 * (self.max_value - hunger) )

    def draw(self):
        for player in self.players.values():
            player.draw()
        self.animation.update()

    def is_over(self):
        for player in self.players.values():
            if not player.is_dead():
                return False
        return True

    def player(self, id):
        if id in self.players.keys():
            return self.players[id]