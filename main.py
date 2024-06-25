import random

import numpy as np
import matplotlib.pyplot as plt
import time

MAX_DISTANCE_RATIO = 1.5
MIN_ATTR = 10
MAX_ATTR = 90
R = 2


def showData(data):
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()


def showClosestPointsConnection(data, connetion):
    plt.scatter(data[:, 0], data[:, 1])
    for point in range(len(data)):
        plt.plot([data[point, 0], data[connetion[point], 0]], [data[point, 1], data[connetion[point], 1]])
    plt.show()


def showClusters(clusters):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    i = 0
    for cluster in clusters:
        for point in cluster:
            plt.scatter(point[0], point[1], color=colors[i])
        i = (i + 1) % 7
    plt.show()


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


def distanceBetweenPoints(x, y):
    return np.sqrt(sum([(x[i] - y[i])**2 for i in range(R) ]))


def findClosestPoints(data):
    connection = [0 for _ in range(len(data))]

    for point in range(len(data)):
        closest = -1
        distance = np.inf
        for candidate in range(len(data)):
            if candidate != point and distance > distanceBetweenPoints(data[point], data[candidate]):
                closest = candidate
                distance = distanceBetweenPoints(data[point], data[candidate])
        connection[point] = closest

    return connection


def connectClosestPoints(data, connetion):
    clustersIndex = 1
    visited = np.zeros_like(connetion)
    clusters = []
    for startingPoint in range(len(data)):
        if visited[startingPoint] == 0:
            cluster = [data[startingPoint]]
            clusterIndex = [startingPoint]
            visited[startingPoint] = clustersIndex
            nextPoint = connetion[startingPoint]
            while True:
                if visited[nextPoint] == 0:
                    cluster.append(data[nextPoint])
                    clusterIndex.append(nextPoint)
                    visited[nextPoint] = clustersIndex
                    nextPoint = connetion[nextPoint]
                elif visited[nextPoint] == clustersIndex:
                    clusters.append(cluster)
                    clustersIndex += 1
                    break
                else:
                    clusters[visited[nextPoint] - 1].extend(cluster)
                    for index in clusterIndex:
                        visited[index] = visited[nextPoint]
                    break
    return clusters


def findClustersToConnect(clusters):
    toConnect = [[] for _ in  range(len(clusters))]

    for i, cluster in enumerate(clusters):
        maxDistanceInCluster = max([distanceBetweenPoints(x, y) for x in cluster for y in cluster]) * MAX_DISTANCE_RATIO
        for y, candidates in enumerate(clusters):
            if i != y:
                flag = 0
                for point in cluster:
                    for candidate in clusters[y]:
                        if maxDistanceInCluster > distanceBetweenPoints(point, candidate):
                            toConnect[i].append(y)
                            flag = 1
                            break
                    if flag == 1:
                        break
    return toConnect


def connectClusters(clusters, toConnect):
    for i, clusterConnections in enumerate(toConnect):
        for connection in clusterConnections:
            if i != connection:
                toConnect[i].extend(toConnect[connection])
                clusters[i].extend(clusters[connection])
                clusters.pop(connection)
                toConnect.pop(connection)
                clusters.insert(connection, [])
                toConnect.insert(connection, [])
    for i, cluster in enumerate(clusters):
        if len(cluster) == 0:
            clusters.pop(i)


def myClusterization(data):
    connection = findClosestPoints(data)
    showClosestPointsConnection(data, connection)
    clusters = connectClosestPoints(data, connection)
    showClusters(clusters)
    clustersNumber = 0

    while clustersNumber != len(clusters):
        clustersNumber = len(clusters)
        toConnect = findClustersToConnect(clusters)
        connectClusters(clusters, toConnect)
        showClusters(clusters)


if __name__ == '__main__':
    data = crateData(random.randint(100, 300), random.randint(3, 6))
    # data = crateData(random.randint(10, 30), random.randint(2, 3))
    showData(data)
    myClusterization(data)


