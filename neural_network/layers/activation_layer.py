from layers.layer import Layer
import numpy as np
from typing import Callable

class ActivationLayer(Layer):
    def __init__(self, activation_func: Callable[[float], float], d_activation_func: Callable[[float], float]) -> None:
        self.activation_func = activation_func
        self.d_activation_func = d_activation_func
    
    def forward_propagate(self, input: np.ndarray) -> np.ndarray:
        self.input = input
        return self.activation_func(input)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * self.d_activation_func(self.input)
