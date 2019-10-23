import matplotlib.pyplot as plt
import numpy as np
import keras.models
from keras.layers import Dense, LSTM
from keras.models import Sequential
from keras.optimizers import Adam
from Player import Player
from Game import Game
from itertools import product

model = Sequential()
# model.add(LSTM(units = 16, batch_input_shape=(1, 1, n_states) ,stateful=True))
model.add(Dense(4, input_shape = (5,), activation='relu', kernel_initializer='random_uniform'))
model.add(Dense(4, kernel_initializer='random_uniform'))
model.compile(loss='mse', optimizer=Adam(lr=0.01))

# model = keras.models.load_model('test2.h5')

game = Game(max_value=30)
gamma = 0.99
player = Player(game)
for (i,j) in product(range(31), repeat=2):
    print(i,j)
    for k in range(10):
        for l in range(11):
            player.stamina = 30 - i
            player.hunger = j
            player.food = k
            player.until_birth = l
            done = not player.stamina or (player.hunger == 30)
            state = np.array([[i, j, k, l, done]])
            target_f = np.array([[0, 0, 0, 0]])
            for action in range(4):
                next_state = np.array([player.next_turn(action)])
                done = player.game.is_over()
                reward = player.game.reward(next_state[0])

                target = reward #+ (1 - done) *  gamma * np.amax(np.take(model.predict(next_state)[0], player.allowed_actions()))
                #target_f = model.predict(state)
                target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)
model.save('test2.h5')

# import keras.models
# import numpy as np

# moves = {0 : 'rest', 1 : 'eat', 2 : 'hunt', 3 : 'reproduce'}
# stats = {0 : 'stamina', 1 : 'hunger', 2 : 'food', 3 : 'until_birth', 4 : 'n_children'}

# model = keras.models.load_model('test.h5')
# print(model.predict(np.array([[30, 25, 0, 0, False]])))