from Player import Player

class Human(Player):

    def next_turn(self, action):

        if action == 0: # Rest
            return self.rest()
        elif action == 1 : #Eat
            return self.eat()
        elif action == 2 : # Hunt
            return self.hunt()
        elif action == 3: # Reproduce
            return self.reproduce()

    def rest(self):
        if self.until_birth == 1:
            n_children = self.n_children() + 1
        else:
            n_children = self.n_children
        if self.until_birth:
            stamina = min(self.stamina + 2, self.max_value)
            hunger = min(2 + self.hunger, self.max_value)
            food = self.food
            until_birth = max(self.until_birth - 1, 0)
        else:
            stamina = min(self.stamina + 4, self.max_value)
            hunger = min(1 + self.hunger, self.max_value)
            food = self.food
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth, n_children

    def eat(self):
        if self.until_birth == 1:
            n_children = self.n_children() + 1
        else:
            n_children = self.n_children
        if self.until_birth:
            stamina = self.stamina
            hunger = max(self.hunger - 3, 0)
            food = max(self.food - 2, 0)
            until_birth = max(self.until_birth - 1, 0)
        else:
            stamina = self.stamina
            hunger = max(self.hunger - 3, 0)
            food = max(self.food - 1, 0)
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth, n_children

    def hunt(self):
        if self.until_birth == 1:
            n_children = self.n_children() + 1
        else:
            n_children = self.n_children
        if self.until_birth:
            food = self.food + 2
            hunger = min(self.hunger + 3, self.max_value)
            stamina = max(self.stamina - 4, 0)
            until_birth = max(self.until_birth - 1, 0)
        else:
            food = self.food + 2
            hunger = min(self.hunger + 2, self.max_value)
            stamina = max(self.stamina - 2, 0)
            until_birth = self.until_birth
        return stamina, hunger, food, until_birth, n_children

    def reproduce(self):
        if self.until_birth == 1:
            n_children = self.n_children() + 1
        else:
            n_children = self.n_children
        if self.until_birth:
            raise Exception("Unallowed action")
        else: 
            stamina = self.stamina
            hunger = self.hunger + 2
            food = self.food
            until_birth = 10
        return stamina, hunger, food, until_birth, n_children