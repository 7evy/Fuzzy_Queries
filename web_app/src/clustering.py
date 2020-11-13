from sklearn.cluster import AgglomerativeClustering
import numpy as np
from utils import *
from operator import add, ne, mul
from pandas import read_csv


Data = read_csv("./data/db_base.csv", sep=";", header=None, engine='c').values.tolist()

FUNCTIONS = [ne, relative_distance, discrete_distance, discrete_distance, relative_distance, ne, ne, ne]

def dist_matrix(data, indexes, Functions):
    M = []
    for x in data :
        M.append(distances(data, indexes, x, Functions))
    return M

def distances(data, indexes, element, Functions):
    """Returns the respective relative distances between element and all data points in Data.
    Takes into account all of the attributes listed in indexes."""
    result = [0 for _ in range(len(data))]
    for attr in indexes :
        result = list(map(add, result, distances_1D(data, attr, element, Functions[attr])))
    return list(np.array(result) / len(indexes))

def distances_1D(data, attr, element, f):
    """Returns the respective relative distances between element and all data points in Data, taking only one attribute into account."""
    dist = []
    for x in data :
        dist.append(f(element[attr], x[attr]))
    return dist

def clustering(data, n_clusters, Functions):
    M = np.asfarray(dist_matrix(data, [k for k in range(len(data[0]))], Functions))
    AC = AgglomerativeClustering(
        n_clusters=n_clusters,
        affinity="precomputed",
        linkage="average"
    )
    return AC.fit_predict(M)

class Clustering():
    Data = []
    Clusters = []
    Functions = []
    n_clusters = 1
    n_attr = 0

    def __init__(self, Data, n_clusters, Functions=[]):
        self.Data = Data
        self.n_clusters = n_clusters
        if Data :
            self.n_attr = len(Data[0])
        self.Functions = Functions + [ne for _ in range(self.n_attr - len(Functions))]
        self.Clusters = clustering(self.Data, self.n_clusters, self.Functions)

    def print_cluster(self, k):
        indexes_to_print = []
        for c in range(len(self.Clusters)):
            if self.Clusters[c] == k :
                indexes_to_print.append(c)
        print("Cluster n°" + str(k) + " contains " + str(len(indexes_to_print)) + " entries :")
        for i in indexes_to_print :
            print(self.Data[i])

    def cluster_distribution(self):
        return [self.Clusters.tolist().count(k) for k in range(self.n_clusters)]

C = Clustering(Data, 15, FUNCTIONS)

C.print_cluster(7)
print(C.cluster_distribution())
