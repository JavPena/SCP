import os
from typing import Any
import numpy as np
import random as r
import pathlib
import math
from os import listdir
from os.path import isfile, join

class Knsapsack:

    def __init__(self) -> None:
        self.maxweigh = 0
        self.profit = []
        self.weigh = []

    def __call__(self, x) -> Any:
        xbin = self.binarize(x)
        xbin = self.repair(xbin)
        return self.objective(xbin)

    def binarize(self, x):
        xbin = [0 for _ in range(len(x))]
        for i in range(len(x)):
            if not (r.random() > 1/(1+math.e**(-2*x[i]))):
                xbin[i] = 1
        return xbin

    def clearData(self):
        self.maxweigh = 0
        self.profit = []
        self.weigh = []

    def constraint(self,individual) -> bool:
        solution = np.asarray(individual)
        sum = np.sum(solution*self.weigh)
        if (sum > self.maxweigh):
            return False
        return True
    
    def objective(self,individual) -> float:
        solution = np.asarray(individual)
        result = np.sum(solution*self.profit)
        return -result
    
    def repair(self,individual) -> list:
        while(self.constraint(individual) == False):
            n = r.randint(0,len(individual)-1)
            individual[n] = 0
        return individual
    
    def instances(self):
        mypath = pathlib.Path(__file__).parent.resolve()
        onlyfiles = [f for f in listdir(mypath) if ((f != os.path.basename(__file__)) and (f != "__pycache__"))]
        return onlyfiles
    
    def readinstance(self,instancename):
        mypath = pathlib.Path(__file__).parent.resolve()
        file = open(str(mypath)+"/"+instancename)
        count = 0
        number = 0
        for line in file:
            for word in line.split():
                word = float(word)
                if count == 0:
                    maxitems = word
                elif count == 1:
                    self.maxweigh = word
                else: 
                    if number == 0:
                        number = 1
                        self.profit.append(word)
                    else:
                        number = number - 1
                        self.weigh.append(word)
                count = count + 1
        self.profit = np.asarray(self.profit)
        self.weigh = np.asarray(self.weigh)
