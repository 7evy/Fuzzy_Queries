from sklearn.cluster import AgglomerativeClustering, AffinityPropagation
import numpy as np
from utils import *
from operator import add, ne, eq
from pandas import read_csv
import matplotlib.pyplot as plt
import dataset as ds


AllData = read_csv("./data/db.csv", sep=";", header=None, engine='c').values.tolist()

Data = [AllData[4*k] for k in range(0, 625)] # Real data

FUNCTIONS = [eq, relative_sim, discrete_sim, discrete_sim, relative_sim, eq, eq, eq, relative_sim, relative_sim, relative_sim] # functions to compute affinities between points
FUNCTIONS2 = [ne, relative_distance, discrete_distance, discrete_distance, relative_distance, ne, ne, ne, relative_distance, relative_distance, relative_distance] # functions to compute distances between points]
INDICES = [1, 4, 8, 9, 10] # attributes to consider for clustering

def dist_matrix(data, indices, Functions):
    """Returns the distance matrix (between each pair of points in data) used for affinity/agglomerative clustering."""
    M = []
    for x in data :
        M.append(distances(data, indices, x, Functions))
    return M

def distances(data, indices, element, Functions):
    """Returns the respective relative distances between element and all data points in Data.
    Takes into account all of the attributes listed in indices."""
    result = [0 for _ in range(len(data))]
    for attr in indices :
        result = list(map(add, result, distances_1D(data, attr, element, Functions[attr])))
    return list(np.array(result) / len(indices))

def distances_1D(data, attr, element, f):
    """Returns the respective relative distances between element and all data points in Data, taking only one attribute into account."""
    dist = []
    for x in data :
        dist.append(f(element[attr], x[attr]))
    return dist

def agglo_clustering(data, n_clusters, indices, Functions):
    """Hierarchical clustering with n_clusters clusters. Returns the labels corresponding to data."""
    M = np.asfarray(dist_matrix(data, indices, Functions))
    AC = AgglomerativeClustering(
        n_clusters=n_clusters,
        affinity="precomputed",
        linkage="average"
    )
    return AC.fit_predict(M)

def agglo_clustering_alt(data, max_dist, indices, Functions):
    """Hierarchical clustering using max_dist as distance threshold. Returns the labels corresponding to data."""
    M = np.asfarray(dist_matrix(data, indices, Functions))
    AC = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=max_dist,
        affinity="precomputed",
        linkage="average"
    )
    return AC.fit_predict(M)

def affinity_clustering(data, indices, Functions, preference):
    """Affinity propagation clustering. Returns the labels corresponding to data, and the computed cluster centers."""
    M = np.asfarray(dist_matrix(data, indices, Functions))
    AC = AffinityPropagation(
        copy=False,
        affinity="precomputed",
        random_state=None,
        preference=preference
    )
    AC.fit(M)
    return AC.labels_, AC.cluster_centers_indices_

class Clustering():
    """Class used to manage the results of affinity propagation and agglomerative clustering."""
    Data = []
    Labels = []
    Centers = []
    indices = []
    Functions = []
    n_clusters = 1

    def __init__(self, Data, Functions=[], indices=[]):
        self.Data = Data
        self.indices = indices if indices else [k for k in range(len(Data[0]))]
        self.Functions = Functions + [ne for _ in range((len(self.indices)) - len(Functions))]

    def by_agglo(self, n_clusters=1):
        """Agglomerative clustering using stored data."""
        self.n_clusters = n_clusters
        self.Labels = agglo_clustering(self.Data, self.n_clusters, self.indices, self.Functions)
    
    def by_affinity(self, preference=None):
        """Affinity propagation clustering using stored data."""
        self.Labels, self.Centers = affinity_clustering(self.Data, self.indices, self.Functions, preference)
        self.n_clusters = len(self.Centers)

    def sort_by_cluster(self):
        """Sorts the dataset by cluster label."""
        zipped = sorted(list(zip(self.Labels, self.Data)))
        self.Labels = [zipped[k][0] for k in range(len(self.Data))]
        self.Data = [zipped[k][1] for k in range(len(self.Data))]

    def mean_dist_centers(self):
        """Returns the mean distance between each cluster and their associated data points. Only works with affinity propagation."""
        if not Centers :
            return "Centers uninitialized"
        centers = []
        for label in set(self.Labels) :
            C = self.cluster(label)
            dist = np.mean(distances(C, self.indices, self.Data[self.Centers[label]], self.Functions))
            centers.append(dist)
        return centers

    def cluster(self, k):
        """Returns the k-th cluster as an array."""
        indexes = []
        for c in range(len(self.Labels)):
            if self.Labels[c] == k :
                indexes.append(c)
        return [Data[i] for i in indexes]

    def print_cluster(self, k):
        """Prints the k-th cluster."""
        C = self.cluster(k)
        print("Cluster n°" + str(k) + " contains " + str(len(C)) + " entries :")
        for x in C :
            print(x)

    def cluster_distribution(self):
        """Returns the number of data points in each cluster."""
        return np.array([self.Labels.tolist().count(k) for k in range(max(self.Labels+1))])

    def centers(self):
        """Returns the cluster centers as an array. Only works with affinity propagation."""
        return [self.Data[c] for c in self.Centers]

    def print_centers(self):
        """Prints every cluster center. Only works with affinity propagation."""
        for c in self.Centers :
            print(self.Data[c])


C = Clustering(Data, FUNCTIONS)
C.by_affinity(-1)
print(C.cluster_distribution())
print(C.n_clusters)

D = ds.Dataset(C.centers(), [eq, relative_sim, discrete_sim, discrete_sim, inf_or_relative, eq, eq, eq, relative_sim, relative_sim, relative_sim], [0, 0.75, 0.5, 0.5, 0.75, 0, 0, 0, 0.75, 0.75, 0.75])

x_axis, y_axis, z_axis = [], [], []
# r_axis, g_axis, b_axis = [], [], []
for x in Data :
    x_axis.append(x[1])
    y_axis.append(x[4])
#     r_axis.append(x[8])
#     g_axis.append(x[9])
#     b_axis.append(x[10])
    z_axis.append(D.choquet(x))
# r_axis = np.array(r_axis)/max(r_axis)
# g_axis = np.array(g_axis)/max(g_axis)
# b_axis = np.array(b_axis)/max(b_axis)
# rgb = [(r_axis[k], g_axis[k], b_axis[k]) for k in range(len(r_axis))]
# fig = plt.figure()
# for i in range(len(x_axis)):
#     msize = 12 if i in C.Centers else 4
#     clr = 'blue' if msize==4 else 'red'
#     plt.plot(x_axis[i], y_axis[i], marker='o', c=clr, markersize=msize)
    # plt.plot(x_axis[i], y_axis[i], marker='o', c=rgb[i], markersize=msize)
# plt.show()
plt.scatter(x_axis, y_axis, marker='o', c=z_axis, cmap=plt.cm.coolwarm)
plt.show()
