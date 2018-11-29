import random
import math


def rand():
    number = random.uniform(-1, 1)
    return number


def sigmoid(x):
    return 1.0 / (1 + math.exp(-x))


def derivative_sigmoid(x):
    return x * (1.0 - x)


class NeuralNetwork:
    def __init__(self, number_inputs, number_hidden, number_outputs, eta):
        self.inputs = number_inputs
        self.hidden_nodes = number_hidden
        self.classes = number_outputs

        self.eta = eta
        self.confidence = 0

        self.bias_bottom = [rand() for i in range(self.hidden_nodes)]
        self.bias_top = [rand() for i in range(self.classes)]
        self.weight_bottom = [[rand() for i in range(self.hidden_nodes)] for j in range(self.inputs)]
        self.weight_top = [[rand() for i in range(self.classes)] for j in range(self.hidden_nodes)]

        self.hidden = [0.0] * self.hidden_nodes
        self.output = [0.0] * self.classes

