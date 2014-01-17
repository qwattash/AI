#!/bin/python

import perceptron
import menu

def max01():
     
    while True:
        x = eval(input("[x vector] (1x{0})>".format(numInputs)))
        if x == []:
            break
        t = eval(input("[t vector] (1x{0})>".format(numOutputs)))
        #xSet.append(x)
        #tSet.append(t)
        #print("[+] training with {x} -> {t}".format(x=x, t=t))
        #p.train(x, t)
        y = p.run(x)
        
        

class Max01Classifier(object):
    
    def __init__(self):
        self.numInputs = 5
        self.numOutputs = 2
        self.p = perceptron.Perceptron(self.numInputs, self.numOutputs, 1)
        self.xSet = [[0,0,0,0,0], 
                     [0,0,0,0,1],
                     [0,0,1,0,0],
                     [1,0,0,0,1],
                     [0,1,0,1,0],
                     [1,0,1,0,1],
                     [0,1,1,1,0],
                     [1,1,0,0,1]]
        self.tSet = [[0,1], 
                     [0,1],
                     [0,1],
                     [0,1],
                     [0,1],
                     [1,0],
                     [1,0],
                     [1,0]]
        self.actions = menu.ActionMenu("Custom Sets")
        self.actions.addItem("train net", lambda m,i: self.trainMenu.run())
        self.actions.addItem("test net", lambda m,i: self.testMenu.run())
        self.trainMenu = menu.PromptMenu(None, self.trainInput)
        self.trainMenu.addItem("insert x vector", menu.arrayParserCallback)
        self.trainMenu.addItem("insert t vector", menu.arrayParserCallback)
        self.testMenu = menu.PromptMenu(None, self.testInput)
        self.testMenu.addItem("insert x vector", menu.arrayParserCallback)

    def run(self):
        e = 1
        count = 0
        maxCount = 10000
        while e > 0.000001 and count < maxCount:
            for i in range(0, len(self.xSet)):
                self.train(self.xSet[i], self.tSet[i])
            e = self.error()
            count += 1
        self.actions.run()
    
    def trainInput(self, menu):
        retval = iter(menu.returnValue.values())
        x = next(retval)
        t = next(retval)
        self.xSet.append(x)
        self.tSet.append(t)
        self.train(x, t)
        self.error()
        print("[+] Updated weights")
        print(self.p)

    def testInput(self, menu):
        x = next(iter(menu.returnValue.values()))
        print("[+] running with {x}".format(x=x))
        y = self.p.run(x)
        print("[+] Output {0}".format(y))
        
    def train(self, x, t):
        print("[+] training with {0} -> {1}".format(x, t))
        self.p.train(x, t)
        
    def error(self):
        Erms = self.p.error(self.xSet, self.tSet)
        print("[+] Error (Erms) reached: {0}".format(Erms))
        return Erms
    
if __name__ == '__main__':
    classifier = Max01Classifier()
    main = menu.ActionMenu("One-layer Perceptron")
    main.addItem("more 1 or 0 test", lambda m,i: classifier.run())
    main.run()
