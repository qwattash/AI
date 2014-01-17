#!/bin/python

import math
import bdn

"""
Single Layer Rosenblatt (1957) Perceptron implementation

The Ronseblatt perceptron always converges to a correct solution, if the
problem can be learned by a single-layer net, no matter how the initial
weights are chosen.
Here such weights are chosen as random positive values in the interval [0, 1]
There is no restriction either on the training rate, however note that a small
training rate resolves to smoother convergence (if the problem can be solved
with a single-layer net).

i) PERCEPTRON PROCESSING UNIT
A simple binary decision neuron (BDN) is used, in which the threshold for the
activation of the neuron is treated as an extra weight (with index 0 in the 
weight list).

The BDN firing function is an Heaviside function, defined as H(t) = (t > 0) ? 1 : 0;
So the output of a single BDN is given by:

y = H(a)
 
with a := activation that is defined as:

a := Sum{j=1:n}( w{j} * x{j} ) - s = Sum{j=0:n}( w{j} * x{j} )

where: 
- s is the activation threshold
- w{j} is the j-th weight, relative to the j-th input Xj
- x{j} is the j-th input (boolean 0 or 1)
- n is the number of inputs (or equivalently weights)

ii) PERCEPTRON LEARNING ALGORITHM
Given a set of P tuples (x, t){p} of input x and desired output t, 
weights are adjusted as follow:

a) select a training pair (x, t){p}, the p-th training pair
b) calculate node output for the input x{p} for each node i

we have that: y{i,p} = H(a{p}) = H( Sum{j=0:n}( w{i,j} * x{j,p} ) )

c) adapt weights on each node i according to the error between y{i,p} and t{i,p}

the new weight w{i,j} = w{i,j} + k * ( t{i,p} - y{i,p} ) * x{j,p}
where k is the training rate.

d) this is generally looped until the error goes to 0 or max epoch is reached.

iii) ERROR
The error is computed as mean squared error.
With an analogous notation as above:

E = 1/(P*N) * Sum{p=1:P}( Sum{i=1:n} (t{i,p} - y{i,p})^2 )

with: 
- P := number of (x,t) pairs in the training set
- N := number of BDN nodes
- t{i,p} is the value of the i-th component of the desired response vector t 
in the p-th pair (x, t)
- y{i,p} is the value of the i-th component of the output response of the net
given the input x in the p-th pair (x, t)

Finally, Erms = sqrt(E)
"""
class Perceptron(object):

    """
    contructor
    @param {int} inputs number of inputs
    @param {int} outputs number of outputs
    @param {double} trainingRate training rate used for weight adaptation for
    learning
    """
    def __init__(self, inputs, outputs, trainingRate):
        #single layer BDN as a list of BDNs
        self.layer0 = [bdn.BDN(inputs) for e in range(0, outputs)]

        self.trainingRate = trainingRate

    """
    training function for supervised learning
    @param {Array.<boolean>} x input vector
    @param {Array.<boolean>} t expected output
    """
    def train(self, x, t):
        #calculate node outputs
        y = self.run(x)
        #for each node, adapt weights according to eta param
        #expand x to count the activation threshold weight
        xx = [1] + x
        #update weights for each node
        for i in range(0, len(self.layer0)):
            node = self.layer0[i]
            for j in range(0, len(node.weights)):
                #print("BDN {0} updating w{1} from {2}".format(i, j, node.weights[j]))
                node.weights[j] = node.weights[j] + self.trainingRate * xx[j] * (t[i] - y[i])
                #print("to {0}".format(node.weights[j]))
    
    """
    error function for supervised learning, calculate error on given training input
    @param {Array.<Array.<boolean>>} xSet input vector set
    @param {Array.<Array.<boolean>>} tSet expected output set
    """
    def error(self, xSet, tSet):
        #mean squared error
        p = len(xSet)
        n = len(self.layer0)
        pSum = 0
        for i in range(0, p):
            nSum = 0
            y = self.run(xSet[i])
            for j in range(0, n):
                nSum += math.pow(tSet[i][j] - y[j], 2)
            pSum += nSum
        Erms = math.sqrt(1/(p*n) * pSum)
        return Erms

    """
    apply a vector and return the answer vector
    @param {Array.<boolean>} x input vector
    @returns {Array.<boolean>} output
    """
    def run(self, x):
        y = []
        for i in range(0, len(self.layer0)):
            y.append(self.layer0[i].run(x))
        return y

    def __repr__(self):
        rep = ""
        for bdn in self.layer0:
            rep += str(bdn)
        return rep
