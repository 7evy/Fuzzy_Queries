from sklearn.cluster import AgglomerativeClustering, AffinityPropagation
import numpy as np
try :
    from fuzzy_queries.static.fuzzy_queries.src.utils import *
except :
    from utils import *
from operator import add, ne, eq
try :
    import fuzzy_queries.static.fuzzy_queries.src.dataset as ds
except :
    import dataset as ds



def dist_matrix(data, indices, Functions):
    """Returns the distance matrix (between each pair of points in data) used for affinity/agglomerative clustering."""
    M = []
    for x in data :
        M.append(distances(data, indices, x, Functions))
    return M

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
    
    FUNCTIONS = [eq, relative_sim, discrete_sim, discrete_sim, relative_sim, eq, eq, eq, relative_sim, relative_sim, relative_sim]
    Data = []
    Labels = []
    Centers = []
    indices = []
    Functions = []
    n_clusters = 1

    def __init__(self, Data, Functions=[], indices=[]):
        self.Data = Data
        self.indices = indices if indices else [k for k in range(len(Data[0]))]
        self.Functions = Functions + [eq for _ in range((len(self.indices)) - len(Functions))]

    def by_agglo(self, n_clusters=1):
        """Agglomerative clustering using stored data."""
        self.n_clusters = n_clusters
        self.Labels = agglo_clustering(self.Data, self.n_clusters, self.indices, self.Functions)
    
    def by_affinity(self, preference=None, n_clusters=0):
        """Affinity propagation clustering using stored data. If a strictly positive n_clusters is given, the algorithm will try to compute this number of clusters +/- 10%."""
        self.Labels, self.Centers = affinity_clustering(self.Data, self.indices, self.Functions, preference)
        if n_clusters > 0 :
            pref = preference
            shift = 0
            count = 1
            for i in range(20):
                if len(self.Centers) <= n_clusters*0.9 :
                    pref += 1/count
                    if shift :
                        count += 1
                    shift = 0
                    self.Labels, self.Centers = affinity_clustering(self.Data, self.indices, self.Functions, pref)
                elif len(self.Centers) >= n_clusters*1.1 :
                    pref -= 1/count
                    if not shift :
                        count += 1
                    shift = 1
                    self.Labels, self.Centers = affinity_clustering(self.Data, self.indices, self.Functions, pref)
                else :
                    break
                if i == 19 :
                    print("Warning : Could not compute", n_clusters, "cluster(s) ! There are", len(self.Centers), "clusters instead.")
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




## Testing and visuals

# from pandas import read_csv
# import matplotlib.pyplot as plt

# AllData = read_csv("../../../../data/db.csv", sep=";", header=None, engine='c').values.tolist()

# Data = [AllData[4*k] for k in range(0, 625)] # Real data

# FUNCTIONS = [eq, relative_sim, discrete_sim, discrete_sim, relative_sim, eq, eq, eq, relative_sim, relative_sim, relative_sim] # functions to compute affinities between points
# FUNCTIONS2 = [ne, relative_distance, discrete_distance, discrete_distance, relative_distance, ne, ne, ne, relative_distance, relative_distance, relative_distance] # functions to compute distances between points]
# INDICES = [1, 4, 8, 9, 10] # attributes to consider for clustering

# C = Clustering(Data, FUNCTIONS)
# C.by_affinity(0.47)
# print(C.n_clusters)

# labels=["Type de logement", "Surface (en m²)", "Nombre de pièces", "Nombre de chambres", "Loyer mensuel (en €)", "Meublé", "Jardin", "Terrasse", "Distance au centre-ville (en m)", "Distance aux transports (en m)", "Distance aux commerces (en m)"]
# ctr = C.centers()
# reduced_ctr = [[c[8], c[4]] for c in ctr]
# reduced_ctr=[[500, 1200], [5000, 450], [2000, 580]]
# reduced_ctr=[[200,20],[800,25],[500,40],[1100,35],[7000,80]]
# D = ds.Dataset(reduced_ctr, [relative_sim, relative_sim], [0.7, 0.7])
# FD = ds.Fuzzy_Dataset(reduced_ctr, [relative_sim, relative_sim])
# D = ds.Dataset(ctr, Dataset.FUNCTIONS, [0, 0.75, 0.5, 0.5, 0.75, 0, 0, 0, 0.75, 0.75, 0.75])
# FD = ds.Fuzzy_Dataset(ctr, Dataset.FUNCTIONS)



## Print attributes value repartition, Choquet scores... etc

# plt.rc('xtick', labelsize=13) 
# plt.rc('ytick', labelsize=13)
# x_axis, y_axis, z_axis = [], [], []
# r_axis, g_axis, b_axis = [], [], []
# for x in AllData :
#     x_axis.append(x[8])
#     y_axis.append(x[1])
    # z_axis.append(FD.choquet([x[8], x[1]]))
    # z_axis.append(FD.nearest_neighbor([x[8], x[1]]))
    # z_axis.append(FD.mean_total_distance([x[8], x[1]]))
#   r_axis.append(x[8])
#   g_axis.append(x[9])
#   b_axis.append(x[10])
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
# _, ax = plt.subplots()
# colorbar = plt.scatter(x_axis, y_axis, marker='o', s=55, c=z_axis, cmap=plt.cm.coolwarm)
# for x in reduced_ctr :
#     plt.plot(x[0], x[1], marker='*', markersize=20, c='lightgreen', markeredgecolor='black')
# plt.colorbar(colorbar, orientation="horizontal").set_label("Degré d'appartenance", fontsize=16)
# plt.xlabel(labels[8], fontsize=16)
# plt.ylabel(labels[1], fontsize=16)
# ax.xaxis.tick_top()
# ax.xaxis.set_label_position("top")
# plt.grid(color='black', alpha=0.1)
# plt.show()



## Print clusters and associated points

# plt.rc('xtick', labelsize=13) 
# plt.rc('ytick', labelsize=13)
# _, ax = plt.subplots()

# colors = ['red', 'black', 'yellow', 'purple', 'pink', 'cyan', 'lightblue', 'lightgreen', 'darkgray', 'darkgreen', 'maroon', 'darkblue', 'darkorange', 'blue']
# for c in range(C.n_clusters):
#     cluster = C.cluster(c)
#     center = C.centers()[c]
#     d = distances(cluster, [4, 8], center, FUNCTIONS)
#     for k in range(len(cluster)):
#         if d[k] > 0.6 :
            # plt.plot(cluster[k][8], cluster[k][4], 'o', markersize=6, markeredgecolor="black", color="darkgray")
#             plt.plot([center[8], cluster[k][8]], [center[4], cluster[k][4]], 'ro-', markersize=6, c=colors[c%13])
#     plt.plot(center[8], center[4], marker='o', markersize=12, c=colors[c%13], markeredgecolor='black')

# ax.xaxis.tick_top()
# ax.xaxis.set_label_position("top")
# plt.xlabel(labels[8], fontsize=16)
# plt.ylabel(labels[4], fontsize=16)
# plt.grid(color='black', alpha=0.1)
# plt.show()
