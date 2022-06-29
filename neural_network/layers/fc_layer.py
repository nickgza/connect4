from layers.layer import Layer
import numpy as np

class FCLayer(Layer):
    def __init__(self, input_size: int, output_size: int) -> None:
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)
    
    def forward_propagate(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return self.weights @ self.input + self.bias

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        weights_gradient = output_gradient @ self.input.T
        input_gradient = self.weights.T @ output_gradient
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return input_gradient
