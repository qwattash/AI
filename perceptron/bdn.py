#!/bin/python

import random

random.seed()

"""
Binary Decision Neuron Model (McCullogh-Pitts Model)
"""
class BDN(object):

    """
    constructor
    @param {int} inputs number of inputs
    @param {Array.<double>} [weights] array of weights for the inputs
    zeroth element in the array is treated as the activation threshold s
    """
    def __init__(self, inputs, weights=None):
        if weights == None:
            #one weight is added for activation
            self.weights = [random.random() for e in range(inputs + 1)]
        else:
            self.weights = weights
        
    """
    apply the input vector x and get the output value for the BDN
    @param {Array.<boolean>} x
    @return boolean
    """
    def run(self, x):
        xx = [1] + x
        #dot product of the input and weights
        dot = sum(map(lambda x,y: x*y, xx, self.weights))
        return dot > 0

    def __repr__(self):
        rep = "BDN\n"
        rep += "Activation {0}\n".format(self.weights[0])
        rep += "Weights {0}\n".format(self.weights[1:])
        return rep
