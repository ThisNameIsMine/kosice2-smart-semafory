import numpy as np

import numpy

from matplotlib import pyplot as plt
from numpy import *
from array import *
class Statictics:
    def __init__(self):
        self.Data=[[[]]]
    @staticmethod
    def chartoriginal(arr):
        counter=1
        for data in arr:
            plt.figure(dpi=100)

            # Creating an array from the list
            x = [el[0] for el in data]
            y = [el[1] for el in data]

            x=[float(i) for i in x]
            y = [float(i) for i in y]
            # Plotting Numpy array

            print(y[len(y)-1])
            plt.plot(x, y)

            # Adding details to the plot
            plt.title('Plot NumPy array')
            plt.xlabel('Time')
            if(counter==1):
                plt.ylabel('Average stop time')
            if (counter==1):
                plt.ylabel('Total stop time')
            # Displaying the plot
            plt.savefig('stats'+str(counter)+'.png')

    @staticmethod
    def chartoptimalized(arr):
        counter = 1
        for data in arr:
            plt.figure(dpi=100)

            # Creating an array from the list
            x = [el[0] for el in data]
            y = [el[1] for el in data]

            x = [float(i) for i in x]
            y = [float(i) for i in y]
            # Plotting Numpy array
            print(y[len(y)-1])
            plt.plot(x, y)

            # Adding details to the plot
            plt.title('Plot NumPy array')
            plt.xlabel('Time')
            if (counter == 1):
                plt.ylabel('Average stop time')
            if (counter == 1):
                plt.ylabel('Total stop time')
            # Displaying the plot
            plt.savefig('statsoptimalized' + str(counter) + '.png')
