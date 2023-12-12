import scipy as sp
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import uncertainties as un
from uncertainties import ufloat
from uncertainties.umath import *
from decimal import *

#-----------
def mprint(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))
    print()
