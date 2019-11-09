from Player import Player

# The possible actions
moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt', 3 : 'reproduce'}
stats = {0 : 'stamina', 1 : 'hunger', 2 : 'food', 3 : 'until_birth', 4 : 'n_children'}
n_moves = len(moves.keys())
n_stats = len(stats.keys())


class Human(Player):

    def next_turn(self, action):

        if action == 0: # Rest
            state = self.rest()
        elif action == 1 : #Eat
            state = self.eat()
        elif action == 2 : # Hunt
            state = self.hunt()
        elif action == 3: # Reproduce
            state = self.reproduce()
        if self.until_birth == 1:
            n_children = self.n_children() + 1
        else:
            n_children = self.n_children()
        return (*state, n_children)

    def rest(self):
        if self.until_birth:
            stamina = min(self.stamina + 2, self.max_value)
            hunger = min(2 + self.hunger, self.max_value)
            food = self.food
            until_birth = max(self.until_birth - 1, 0)
        else:
            stamina = min(self.stamina + 4, self.max_value)
            hunger = min(self.hunger + 1, self.max_value)
            food = self.food
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth

    def eat(self):
        if self.until_birth:
            stamina = self.stamina
            hunger = max(self.hunger - 3, 0)
            food = self.food - 2
            until_birth = max(self.until_birth - 1, 0)
        else:
            stamina = self.stamina
            hunger = max(self.hunger - 3, 0)
            food = self.food - 1
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth

    def hunt(self):
        if self.until_birth:
            food = min(self.food + 2, self.max_value)
            hunger = min(self.hunger + 3, self.max_value)
            stamina = max(self.stamina - 4, 0)
            until_birth = max(self.until_birth - 1, 0)
        else:
            food = min(self.food + 2, self.max_value)
            hunger = min(self.hunger + 2, self.max_value)
            stamina = max(self.stamina - 2, 0)
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth

    def reproduce(self):
        if self.until_birth:
            raise Exception("Unallowed action")
        else: 
            stamina = self.stamina
            hunger = self.hunger + 2
            food = self.food
            until_birth = 10
        return stamina, hunger, food, until_birth

    def is_dead(self):
        """ Return True if the player is dead and False otherwise"""
        return self.stamina <= 0 or self.hunger >= self.max_value or self.age >= 100 or self.food < 0