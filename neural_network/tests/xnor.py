import sys
sys.path.append('..')
import numpy as np
from layers.fc_layer import *
from layers.activation_funcs import *
import loss_funcs
from network import Network
import matplotlib.pyplot as plt

X = np.reshape([0, 0, 0, 1, 1, 0, 1, 1], (4, 2, 1))
Y = np.reshape([1, 0, 0, 1], (4, 1, 1))

network = Network([
    FCLayer(2, 3),
    ELU(),
    FCLayer(3, 1),
    ELU(),
])

network.train(loss_funcs.mean_squared, loss_funcs.d_mean_squared, X, Y, epochs=1000)

points = np.array([(x, y, network.predict(np.reshape([x, y], (2, 1))).item(0)) for x in np.linspace(0, 1, 20) for y in np.linspace(0, 1, 20)])

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=points[:, 2], cmap="winter")
plt.show()
