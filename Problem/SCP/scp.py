import os
from typing import Any
import numpy as np
import random as r
import pathlib
import math
from os import listdir
from os.path import isfile, join

class SCP:

    def __init__(self) -> None:
        self.a = [[]]
        self.cost = []
        self.rows = 0
        self.columns = 0

    def __call__(self, x) -> Any:
        xbin = self.binarize(x)
        xbin = self.repair(xbin)
        return self.objective(xbin)
    
    def clearData(self):
        self.a = [[]]
        self.cost = []
        self.rows = 0
        self.columns = 0

    def binarize(self, x):
        xbin = [0 for _ in range(len(x))]
        for i in range(len(x)):
            if not (r.random() > 1/(1+math.e**(-x[i]))):
                xbin[i] = 1
        return xbin

    def constraint(self,individual) -> bool:
        indices = list(range(self.rows))
        r.shuffle(indices)
        for i in indices:
            sum = np.sum(self.a[i]*np.asarray(individual))
            if (sum == 0):
                return False
        return True
    
    def objective(self,individual) -> float:
        solution = np.asarray(individual)
        result = np.sum(solution*self.cost)
        return result
    
    def repair(self,individual) -> list:
        while(self.constraint(individual) == False):
            indices = list(range(self.rows))
            r.shuffle(indices)
            for i in indices:
                while np.sum(self.a[i] * np.asarray(individual)) < 1:
                    idxRestriccion = np.argwhere(np.asarray(self.a[i]) > 0)
                    r.shuffle(idxRestriccion)
                    individual[idxRestriccion[0][0]] = 1
        return individual
        
    def instances(self):
        mypath = pathlib.Path(__file__).parent.resolve()
        onlyfiles = [f for f in listdir(mypath) if (f != os.path.basename(__file__))]
        return onlyfiles

    def readinstance(self,filename):
        mypath = pathlib.Path(__file__).parent.resolve()
        file = open(str(mypath)+"/"+filename)
        count = 0
        c = -1
        number = 0
        for line in file:
            for word in line.split():
                word = int(word)
                if count == 0:
                    self.rows = word
                elif count == 1:
                    self.columns = word
                    self.a = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
                elif count < self.columns + 2:
                    self.cost.append(word)
                else: 
                    if number == 0:
                        number = word
                        c = c + 1
                    else:
                        self.a[c][word-1] = 1
                        number = number - 1
                count = count + 1
                

