#!/usr/bin/python
import numpy

matri_x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
matri_x = numpy.array(matri_x, dtype = numpy.int8)
h= [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
h = numpy.array(h, dtype = numpy.int8)
matrix_out = numpy.zeros((3, 3,), dtype = numpy.int8)

for i in range(len(matri_x)):
  for j in range(len(matri_x[0])):
    suma = 0
    for n in range(i-1, i+2):
      for m in range(j-1, j+2):
        try:
          if n >= 0 and m >= 0 and n < len(matri_x[0]) and m < len(matri_x):
            suma += h[n - (i - 1), m - (j - 1)] * matri_x[n, m]
        except IndexError:
          suma += 0
          matrix_out[i, j] = suma
print (matrix_out)
