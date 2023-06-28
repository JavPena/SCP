from typing import Any
from zellij.core import ArrayVar, FloatVar, Loss, Experiment, Threshold
from zellij.strategies import PHS, ILS, DBA
from zellij.strategies.tools import Hypersphere, Distance_to_the_best, Move_up
from zellij.utils.converters    import FloatMinmax, ArrayConverter, Basic

import numpy as np
from Problem.SCP.scp import SCP

problem = SCP()

data = problem.readinstance()


lf = Loss()(problem)
values = ArrayVar(converter=ArrayConverter())

for i in range(len(problem.cost)):
    values.append(FloatVar("float_"+str(i), -5 , 5, converter=FloatMinmax()),)

sp = Hypersphere(values, lf, converter=Basic())


explor = PHS(sp, inflation=1.75)
exploi = ILS(sp, inflation=1.75)
stop1 = Threshold(None, "current_calls", 3)  # set target to None, DBA will automatically asign it.
stop2 = Threshold(None,"current_calls", 100)  # set target to None, DBA will automatically asign it.
dba = DBA(sp, Move_up(sp,5),(explor,stop1), (exploi,stop2),scoring=Distance_to_the_best())

stop3 = Threshold(lf, "calls",10000)


exp = Experiment(dba, stop3, save=data, backup_interval=5)
exp.run()
print(f"Best solution:f(x)={lf.best_score}")


