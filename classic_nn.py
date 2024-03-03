import traceback
from datetime import datetime

import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten, Reshape

import chess

def main():

    x_train = np.load("x_train.npy")
    y_train = np.load("y_train.npy")
    x_test = np.load("x_test.npy")
    y_test = np.load("y_test.npy")

    print("shapes: ")
    print("x_train", x_train.shape)
    print("y_train", y_train.shape)
    print("x_test", x_test.shape)
    print("y_test", y_test.shape)


    def weighted_mse(y_true, y_pred):
        weights = (y_true * 62) + 1
        squared_difference = tf.math.multiply(weights, tf.square(y_true - y_pred))
        return tf.reduce_mean(squared_difference)


    def max_criterion(arr):
        positions = np.transpose(np.unravel_index(np.argsort(arr[0], axis=None)[::-1], arr[0].shape))
        moves = np.transpose(np.unravel_index(np.argsort(arr[1], axis=None)[::-1], arr[1].shape))

        positions = np.repeat(positions, 64, axis=0)
        moves = np.tile(moves, (64, 1))
        res = np.hstack((positions, moves))
        return res


    def harmonic_criterion(arr):

        new_array = np.zeros((8*8*8*8, 5))

        for pos_row in range(8):
            for pos_col in range(8):
                for mov_row in range(8):
                    for mov_col in range(8):
                        harmonic_mean = ((2*arr[0][pos_row][pos_col]*arr[1][mov_row][mov_col]) /
                                         (arr[0][pos_row][pos_col] + arr[1][mov_row][mov_col]))
                        new_array[(pos_row*8 + pos_col)*64 + 8*mov_row + mov_col] = \
                            [pos_row, pos_col, mov_row, mov_col, harmonic_mean]

        sorted_moves = new_array[np.argsort(new_array[:, 4])[::-1]]

        return sorted_moves[:, :-1].astype(int)




    for i,layer_set in enumerate([


                                (Dense(32, activation='tanh'),
                                 Dense(32, activation='tanh'),
                                 Dense(32, activation='tanh'),
                                 Dense(8 * 8 * 2, activation='sigmoid'))
                                 ]):

        model = Sequential()
        model.add(Flatten(input_shape=(12,8,8)))
        for layer in layer_set:
            model.add(layer)

        model.add(Reshape((2, 8, 8)))

        #model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.compile(loss=weighted_mse, optimizer='adam', metrics=['accuracy'])


        model.fit(x_train, y_train, epochs=10, batch_size=4, verbose=0)
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        model.save(f"{current_time}.keras")


        loss, accuracy = model.evaluate(x_test, y_test)

        predictions = model.predict(x_test)

        number_of_tries = []

        for board, pred in zip(x_test, predictions):
            chess_game_white = chess.Chess()
            chess_game_white.load_board(board, 1)
            chess_game_black = chess.Chess()
            chess_game_black.load_board(board, 0)



            predicted_moves = harmonic_criterion(pred)

            for row_index, move_numbers in enumerate(predicted_moves):
                try:
                    if chess_game_white.is_move_valid(*move_numbers) or chess_game_black.is_move_valid(*move_numbers):
                        #print(move_numbers)
                        number_of_tries.append(row_index)
                        break
                except Exception as e:
                    print(board)
                    print(move_numbers)
                    input()
                    traceback.print_exc()
                    print(e)
                    print()

        print(i, accuracy, sum(number_of_tries)/len(number_of_tries))

if __name__ == "__main__":
    main()