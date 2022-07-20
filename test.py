from multiprocessing import Process, Array
import time
import numpy as np


def printArr(pos):
    print(len(pos))
    print(pos[0][0])
    print(pos[1][1])
    print(pos[2][2])


if __name__ == '__main__':
    pos = Array('f', range(9))
    print(np.array(pos))
