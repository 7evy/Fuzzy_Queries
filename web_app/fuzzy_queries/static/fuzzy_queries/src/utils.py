from operator import *
import numpy as np
try :
    import fuzzy_queries.static.fuzzy_queries.src.dataset as ds
except :
    import dataset as ds

def discrete_distance(x, y):
    """Distance between small integers."""
    if x == y :
        return 0
    elif abs(x-y) == 1 :
        return 0.5
    else :
        return 1

def discrete_sim(x, y):
    return 1 - discrete_distance(x, y)

def relative_distance(x, y):
    """Relative distance between x and y, in [0;1]."""
    return 0 if x == y else abs(x-y)/max(x, y)

def relative_sim(x, y):
    """Complement of the normalized distance between x and y, in [0;1]."""
    return 1 - relative_distance(x, y)

def inf_or_relative(x, y):
    """Useful if x < y is as good as x == y."""
    return 1 if x <= y else relative_sim(x, y)

F = [eq, eq, relative_sim, discrete_sim, discrete_sim, inf_or_relative, eq, eq, eq, relative_sim, relative_sim, relative_sim]
T = [0, 0, 0.75, 0.5, 0.5, 0.75, 0, 0, 0, 0.75, 0.75, 0.75]

def random_selection(data, n):
    sel = [data[k] for k in np.random.randint(0, len(data), n)]
    D = ds.Dataset(sel, F, T)
    return sel, D.select_most_satisfying(data, 20)
