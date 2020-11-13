from sklearn.cluster import AgglomerativeClustering
import numpy as np
from utils import *
from operator import add, ne, mul



Test = [["Appartement",45.1,2,1,621,0,0,0,1689,820,2126],
        ["Appartement",91.2,5,4,1824,1,0,0,60,22,1145],
        ["Maison",90.5,5,4,788,0,1,0,991,361,122],
        ["Maison",112.2,5,3,1020,1,0,0,3279,853,2950],
        ["Appartement",42.6,2,1,414,0,0,0,3745,1146,2919],
        ["Studio",27.7,2,1,294,1,0,1,836,426,2588],
        ["Studio",26.3,1,1,341,1,0,0,2004,1444,4499],
        ["Appartement",82.0,3,2,676,1,0,0,2964,1307,250],
        ["Appartement",77.7,3,2,634,1,0,0,3443,805,3684],
        ["Appartement",42.6,2,1,425,1,0,0,2639,1268,2329]]

N_CLUSTERS = 10
FUNCTIONS = [ne, relative_distance, discrete_distance, discrete_distance, relative_distance, ne, ne, ne, relative_distance, relative_distance, relative_distance]

def dist_matrix(data, indexes, Functions):
    M = []
    for x in data :
        M.append(distances(data, indexes, x, Functions))
    return M

def distances(data, indexes, element, Functions):
    """Returns the respective relative distances between element and all data points in Data.
    Takes into account all of the attributes listed in indexes."""
    l = len(indexes)
    result = [0 for _ in range(l)]
    for attr in indexes :
        result = list(map(add, result, distances_1D(data, attr, element, Functions[attr])))
    return list(np.array(result) / l)

def distances_1D(data, attr, element, f):
    """Returns the respective relative distances between element and all data points in Data, taking only one attribute into account."""
    dist = []
    for x in data :
        dist.append(f(element[attr], x[attr]))
    return dist

def clusters(data):
    M = np.asfarray(dist_matrix(data, [k for k in range(len(data[0]))], FUNCTIONS))
    AC = AgglomerativeClustering(
        n_clusters=N_CLUSTERS,
        affinity="precomputed",
        linkage="average"
    )
    return AC.fit_predict(M)

print(clusters(Test))
