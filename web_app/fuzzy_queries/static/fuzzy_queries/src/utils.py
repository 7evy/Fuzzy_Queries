from operator import *
import numpy as np


def discrete_distance(x, y):
    """Distance between small integers."""
    if x == y :
        return 0
    elif abs(x-y) == 1 :
        return 0.5
    else :
        return 1

def discrete_sim(x, y):
    """Similarity between small integers."""
    return 1 - discrete_distance(x, y)

def relative_distance(x, y):
    """Relative distance between x and y, in [0;1]."""
    return 0 if x == y else abs(x-y)/max(x, y)

def relative_sim(x, y):
    """Complement of the normalized distance between x and y, in [0;1]."""
    return 1 - relative_distance(x, y)

def inf_or_relative(x, y):
    """Useful if x < y is as good as x == y."""
    return 1 if x < y else relative_sim(x, y)

def distances(data, indices, element, Functions):
    """Returns the respective relative distances between element and all data points in data.
    Takes into account all of the attributes listed in indices."""
    result = [0 for _ in range(len(data))]
    for attr in indices :
        result = list(map(add, result, distances_1D(data, attr, element, Functions[attr])))
    return list(np.array(result) / len(indices))

def distances_1D(data, attr, element, f):
    """Returns the respective relative distances between element and all data points in data, taking only one attribute into account."""
    dist = []
    for x in data :
        dist.append(f(element[attr], x[attr]))
    return dist
