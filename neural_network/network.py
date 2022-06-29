from layers.layer import Layer

class Network:
    def __init__(self, *network: tuple[Layer] | tuple[list[Layer]] | None):
        if network is None:
            self.network = []
        elif type(network[0]) is list:
            if len(network) == 1:
                self.network = network[0]
            else:
                raise ValueError
        else:
            if all(isinstance(layer, Layer) for layer in network):
                self.network = list(network)
            else:
                raise ValueError

    def add_layers(self, *layers: tuple[Layer] | tuple[list[Layer]] | None):
        if layers is None:
            return
        elif type(layers[0]) is list:
            if len(layers) == 1:
                self.network.extend(layers[0])
            else:
                raise ValueError
        else:
            if all(isinstance(layer, Layer) for layer in layers):
                self.network.extend(list(layers))
            else:
                raise ValueError

    def predict(self, input):
        output = input
        for layer in self.network:
            output = layer.forward_propagate(output)
        return output

    def train(self, loss_func, d_loss_func, x_data, y_data, epochs=1000, learning_rate=0.1, verbose=True):
        for epoch in range(epochs):
            error = 0
            for x, y in zip(x_data, y_data):
                # forward
                output = self.predict(x)

                # error
                error += loss_func(y, output)

                # backward
                grad = d_loss_func(y, output)
                for layer in reversed(self.network):
                    grad = layer.backward_propagate(grad, learning_rate)

            error /= len(x_data)
            if verbose:
                print(f"{epoch + 1}/{epochs}, {error=}")
