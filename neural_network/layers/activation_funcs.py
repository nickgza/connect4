from layers.activation_layer import ActivationLayer
from layers.layer import Layer
import numpy as np

class Tanh(ActivationLayer):
    def __init__(self):
        tanh = lambda A: np.tanh(A)
        d_tanh = lambda A: 1 - np.tanh(A) ** 2
        super().__init__(tanh, d_tanh)

class Sigmoid(ActivationLayer):
    def __init__(self):
        sigmoid = lambda A: 1 / (1 + np.exp(-A))
        d_sigmoid = lambda A: (s := sigmoid(A)) * (1 - s)
        super().__init__(sigmoid, d_sigmoid)

class Swish(ActivationLayer):
    def __init__(self):
        swish = lambda A: A / (1 + np.exp(-A))
        d_swish = lambda A: swish(A) + (1 / (1 + np.exp(-A))) * (1 - swish(A))
        super().__init__(swish, d_swish)

class ReLU(ActivationLayer):
    def __init__(self):
        relu = lambda A: np.fmax(A, 0)
        d_relu = lambda A: np.heaviside(A, 1)
        super().__init__(relu, d_relu)

class ELU(ActivationLayer):
    def __init__(self):
        elu = lambda A: np.vectorize(lambda x: x if x >= 0 else np.exp(x) - 1)(A)
        d_elu = lambda A: np.vectorize(lambda x: 1 if x >= 0 else np.exp(x))(A)
        super().__init__(elu, d_elu)

class Softmax(Layer):
    def forward_propagate(self, input):
        self.output = (output := np.exp(input)) / np.sum(output)
        return self.output

    def backward_propagate(self, output_gradient, learning_rate):
        return ((np.identity(np.size(self.output)) - self.output.T) * self.output) @ output_gradient
