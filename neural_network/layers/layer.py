from abc import ABC, abstractmethod

class Layer(ABC):
    def __init__(self):
        self.input = None
        self.output = None
    
    @abstractmethod
    def forward_propagate(self, input):
        pass

    @abstractmethod
    def backward_propagate(self, output_gradient, learning_rate):
        pass
