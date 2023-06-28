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
        self.example = 0

    def __call__(self, x) -> Any:
        if(self.example == 0):
            print(x)
            self.example = 1
        xbin = self.binarize(x)
        xbin = self.repair(xbin)
        return self.objective(xbin)

    def binarize(self, x):
        xbin = [0 for _ in range(len(x))]
        for i in range(len(x)):
            if not (r.random() > 1/(1+math.e**(-x[i]))):
                xbin[i] = 1
        return xbin

    def constraint(self,individual) -> bool:
        for i in range(len(self.a[0])):
            sum = 0
            for j in range(len(self.a)):
                sum = sum + self.a[j][i]*individual[j]
            if (sum == 0):
                return False
        return True
    
    def objective(self,individual) -> float:
        solution = np.asarray(individual)
        result = np.sum(solution*self.cost)
        print(result)
        return result
    
    def repair(self,individual) -> list:
        print("repair")
        while(self.constraint(individual) == False):
            n = r.randint(0,len(individual)-1)
            if(individual[n] == 0):
                individual[n] = 0
            else:
                individual[n] = 1
        print("finish repair")
        return individual
    
    def readinstance(self):
        mypath = pathlib.Path(__file__).parent.resolve()
        onlyfiles = [f for f in listdir(mypath)]
        for f in onlyfiles:
            if(f != os.path.basename(__file__) ) and (f.split(".")[1] != "csv") and (not os.path.isfile(str(mypath)+"/"+f.split(".")[0]+".csv")):
                file = open(str(mypath)+"/"+f)
                data = open(str(mypath)+"/"+f.split(".")[0]+".csv","a")
                count = 0
                c = -1
                number = 0
                for line in file:
                    for word in line.split():
                        word = int(word)
                        if count == 0:
                            rows = word
                        elif count == 1:
                            columns = word
                            self.a = [[0 for _ in range(columns)] for _ in range(rows)]
                        elif count < columns + 2:
                            self.cost.append(word)
                        else: 
                            if number == 0:
                                number = word
                                c = c + 1
                            else:
                                self.a[c][word-1] = 1
                                number = number - 1
                        count = count + 1
                break
        return f.split(".")[0]
                




           

