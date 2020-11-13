from numpy import mean, sqrt



def discrete_distance(x, y):
    """Distance between small integers."""
    if x == y :
        return 0
    elif abs(x-y) == 1 :
        return 0.5
    else :
        return 1

def relative_distance(x, y):
    """Relative distance between x and y, in [0;1]."""
    return 0 if x == y else abs(x-y)/max(x, y)

def relative_sim(x, y):
    """Complement of the normalized distance between x and y, in [0;1]."""
    return 1 - relative_distance(x, y)

def inf_or_relative(x, y):
    """Useful if x < y is as good as x == y."""
    return 1 if x <= y else relative_sim(x, y)