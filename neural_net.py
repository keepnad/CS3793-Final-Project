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
    def __init__(self, eta):
        self.inputs = 300
        self.hidden_nodes = 20
        self.outputs = 5

        self.eta = eta
        self.confidence = 0

        self.bias_bottom = [rand() for __ in range(self.hidden_nodes)]
        self.bias_top = [rand() for __ in range(self.outputs)]
        self.weight_bottom = [[rand() for __ in range(self.hidden_nodes)] for j in range(self.inputs)]
        self.weight_top = [[rand() for __ in range(self.outputs)] for j in range(self.hidden_nodes)]

        self.hidden = [0.0] * self.hidden_nodes
        self.output = [0.0] * self.outputs

    def predict(self, sample):
        i = 0
        for k in range(self.hidden_nodes):
            weight_sum = 0.0
            for i in range(self.inputs):
                weight_sum += self.weight_bottom[i][k] * sample[i]
            weight_sum += self.bias_bottom[k]
            self.hidden[k] = sigmoid(weight_sum)

        for k in range(self.outputs):
            weight_sum = 0.0
            for i in range(self.hidden_nodes):
                weight_sum += self.weight_top[i][k] * self.hidden[i]
            weight_sum += self.bias_top[k]
            self.output[k] = sigmoid(weight_sum)

        for k in range(self.outputs):
            if k == 0 or self.output[k] > self.output[i]:
                i = k

        next_max_sum = -1.0
        for k in range(self.outputs):
            if k != i:
                if next_max_sum < 0.0 or self.output[k] > next_max_sum:
                    next_max_sum = self.output[k]
        self.confidence = self.output[i] - next_max_sum

        return i

        # if i == 0:
        #     return 'noun'
        # elif i == 1:
        #     return 'verb'
        # elif i == 2:
        #     return 'adjective'
        # elif i == 3:
        #     return 'adverb'
        # elif i == 4:
        #     return 'preposition'

    def adjust_weights(self, sample, actual):
        delta = [0] * self.outputs
        for k in range(self.outputs):
            if k == actual:
                weight_sum = 1.0
            else:
                weight_sum = 0.0
            weight_sum -= self.output[k]

            delta[k] = weight_sum * derivative_sigmoid(self.output[k])

            for i in range(self.hidden_nodes):
                self.weight_top[i][k] += self.eta * delta[k] * self.hidden[i]

            self.bias_top[k] += self.eta * delta[k]

        for j in range(self.hidden_nodes):
            d = 0.0
            for k in range(self.outputs):
                d += self.weight_top[j][k] * delta[k]

            for i in range(self.inputs):
                self.weight_bottom[i][j] += self.eta * derivative_sigmoid(self.hidden[j]) * d * sample[i]

            self.bias_bottom[j] += self.eta * d
