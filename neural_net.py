# Daniel Peek qer419
# Michael Canas ohh135
# CS 3793 Final Project
# 12/4/18
# neural_net.py based on code provided by Dr. O'Hara for assignment 4

import random
import math

# generate random values for initializing weights
def rand():
    number = random.uniform(-1, 1)
    return number


# logistic sigmoid function
def sigmoid(x):
    return 1.0 / (1 + math.exp(-x))


# derivative of sigmoid
def derivative_sigmoid(x):
    return x * (1.0 - x)


# Neural network class, contains functions to train network
class NeuralNetwork:
    def __init__(self, eta):
        # 1 input for each dimension of Word2Vec vector
        self.inputs = 300
        # Just guessed for this number, seems to work
        self.hidden_nodes = 20
        # 1 output for each part of speech looked for
        self.outputs = 5

        # learning rate
        self.eta = eta

        # initialize weights randomly
        self.bias_bottom = [rand() for __ in range(self.hidden_nodes)]
        self.bias_top = [rand() for __ in range(self.outputs)]
        self.weight_bottom = [[rand() for __ in range(self.hidden_nodes)] for ___ in range(self.inputs)]
        self.weight_top = [[rand() for __ in range(self.outputs)] for ___ in range(self.hidden_nodes)]

        self.hidden = [0.0] * self.hidden_nodes
        self.output = [0.0] * self.outputs

    # feed forward prediction
    def predict(self, sample):
        i = 0
        # feed from inputs to hidden nodes
        for k in range(self.hidden_nodes):
            weight_sum = 0.0
            for i in range(self.inputs):
                weight_sum += self.weight_bottom[i][k] * sample[i]
            weight_sum += self.bias_bottom[k]
            self.hidden[k] = sigmoid(weight_sum)

        # feed from hidden nodes to outputs
        for k in range(self.outputs):
            weight_sum = 0.0
            for i in range(self.hidden_nodes):
                weight_sum += self.weight_top[i][k] * self.hidden[i]
            weight_sum += self.bias_top[k]
            self.output[k] = sigmoid(weight_sum)

        # find highest activation, that is the guess
        for k in range(self.outputs):
            if k == 0 or self.output[k] > self.output[i]:
                i = k

        return i

        # return value meanings;
        # 0 = noun
        # 1 = verb
        # 2 = adjective
        # 3 = adverb
        # 4 = preposition

    # backwards propagation to train weights
    def adjust_weights(self, sample, actual):
        delta = [0] * self.outputs

        # from outputs to hidden nodes
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

        # from hidden nodes to inputs
        for j in range(self.hidden_nodes):
            d = 0.0
            for k in range(self.outputs):
                d += self.weight_top[j][k] * delta[k]

            for i in range(self.inputs):
                self.weight_bottom[i][j] += self.eta * derivative_sigmoid(self.hidden[j]) * d * sample[i]

            self.bias_bottom[j] += self.eta * d
