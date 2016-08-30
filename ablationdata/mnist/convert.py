#!/usr/bin/python
import sys
import numpy
import math

f = open(sys.argv[1], 'rb') # opens the csv file
matrix = numpy.loadtxt(open(sys.argv[1],"rb"),delimiter=",",skiprows=0)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        print "{} {} {}".format(i, j, float(matrix[i][j])/2500)
    print
