import random

import numpy as np
import matplotlib.pyplot as plt
import time

MIN_ATTR = 10
MAX_ATTR = 90
R = 2

def crateData(numOfObj, numOfClusters):
    data = np.zeros((numOfObj, R))

    strengthRatio = np.random.randint(1, 10, size=numOfClusters)
    sumStrenghRatio = sum(strengthRatio)
    numOfObjInCluster = numOfObj * strengthRatio / sumStrenghRatio

    if sum([round(numOfObjInCluster[i]) for i in range(numOfClusters)]) > numOfObj:
        numOfObjInCluster[0] -= 1

    i = 0
    for cluster in range(numOfClusters):
        data[i, 0] = random.random() * (MAX_ATTR - MIN_ATTR) + MIN_ATTR
        data[i, 1] = random.random() * (MAX_ATTR - MIN_ATTR) + MIN_ATTR
        i += 1
        for obj in range(round(numOfObjInCluster[cluster]) - 1):
            data[i, 0] = data[i - 1, 0] + random.random() * 4 - 2
            data[i, 1] = data[i - 1, 1] + random.random() * 4 - 2
            i += 1
    np.random.shuffle(data)
    return data


if __name__ == '__main__':
    data = crateData(200, random.randint(3, 6))
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
