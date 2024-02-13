import numpy as np
from keras.models import Sequential
from keras.layers import Dense

import chess

with open("res2.txt") as f:
    games = f.readlines()

games_train = games[:int(len(games)*0.8)]
games_test = games[int(len(games)*0.8):]


def code_games(games_list):
    x = np.zeros((0))
    y = np.zeros((0))

    for i, game in enumerate(games_list):
        color = i % 2
        chess_game = chess.Chess()
        chess_game.reset_board()
        print(i)

        for j, move in enumerate(game.split(",")):
            print(i, j)
            move = move.replace("\n","")
            coded_move = chess_game.move_notation_to_digits(move)
            if j % 2 != color:
                board = chess_game.code_board(color)
                current_move = chess_game.code_move(*coded_move)


                x = board if not len(x) else np.concatenate((x, board))
                y = current_move if not len(y) else np.concatenate((y, current_move))


            chess_game.move_piece(*coded_move)
            chess_game.turn = 1 - chess_game.turn
    return x, y


x_train, y_train = code_games(games_train)
x_test, y_test = code_games(games_test)

print("shapes: ")
print("x_train", x_train.shape)
print("y_train", y_train.shape)
print("x_test", x_test.shape)
print("y_test", y_test.shape)

model = Sequential()
model.add(Dense(32, input_shape=(12, 8, 8), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(8*8*2, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


model.fit(x_train, y_train, epochs=1, verbose=1)


loss, accuracy = model.evaluate(x_test, y_test)
print(f"Training Accuracy: {accuracy}")


predictions = model.predict(X_train)
print("Predictions:")
print(predictions)
