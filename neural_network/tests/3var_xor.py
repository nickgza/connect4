import sys
sys.path.append('..')
import numpy as np
from layers.fc_layer import *
from layers.activation_funcs import *
import loss_funcs
from network import Network
from pprint import pprint

X = np.reshape([0, 0, 0,
                0, 0, 1,
                0, 1, 0,
                0, 1, 1,
                1, 0, 0,
                1, 0, 1,
                1, 1, 0,
                1, 1, 1,], (8, 3, 1))
Y = np.reshape([0, 1, 1, 0, 1, 0, 0, 1], (8, 1, 1))

network = Network([
    FCLayer(3, 5),
    Tanh(),
    FCLayer(5, 1),
    Tanh(),
])

network.train(loss_funcs.mean_squared, loss_funcs.d_mean_squared, X, Y, epochs=5000, learning_rate=0.1)

pprint([(x, y, z, round(network.predict(np.reshape([x, y, z], (3, 1))).item(0), 4)) for x in [0, 1] for y in [0, 1] for z in [0, 1]])
