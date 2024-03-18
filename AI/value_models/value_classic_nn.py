from datetime import datetime

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Flatten


def rescale_y(y):
    return ((y+1)/2.1)*2-1


def main():

    x_train = np.load("x_train2.npy")
    y_train = rescale_y(np.load("y_train2.npy"))
    x_test = np.load("x_test2.npy")
    y_test = rescale_y(np.load("y_test2.npy"))

    print("shapes: ")
    print("x_train", x_train.shape)
    print("y_train", y_train.shape)
    print("x_test", x_test.shape)
    print("y_test", y_test.shape)

    for i, layer_set in enumerate([
                                (Dense(32, activation='tanh'),
                                 Dense(32, activation='tanh'),
                                 Dense(32, activation='tanh'),
                                 Dense(1, activation='tanh'))
                                 ]):

        model = Sequential()
        model.add(Flatten(input_shape=(12, 8, 8)))
        for layer in layer_set:
            model.add(layer)

        model.compile(loss="mean_squared_error", optimizer='adam')

        model.fit(x_train, y_train, epochs=1, batch_size=4, verbose=1)
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        model.save(f"value_nn_{current_time}.keras")
        loss = model.evaluate(x_test, y_test)
        print("test_loss", loss)


if __name__ == "__main__":
    main()
