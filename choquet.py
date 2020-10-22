


Test = [[2, 2, 2], [3, 3, 3], [2, 2, 3]]

def equals(a, b) :  # Default function
    return a == b

def delta(Set, attr, value, function=equals, threshold=0):
    """Measures the proportion of elements in Set (2D array), of which attribute attr satisfies the condition : function(attr, value) > threshold.
    By default, the condition is strict equality."""
    ret = 0
    for x in Set :
        if function(x[attr], value) > threshold :
            ret += 1
    return ret/len(Set)

def mu(Set, Properties, Functions=[], Thresholds=[]):
    """Returns the maximal similarity between an element of Set (2D array) and Properties (subset of attributes and values).
    The score is 1 if there is x in Set which, for all tuples in Properties, verifies : function(attribute, value) > threshold.
    The function and threshold are taken from their respective lists, and default to equality and 0 (i.e the default condition is strict equality)."""
    score = 0
    m, n, l = len(Properties), len(Functions), len(Thresholds)
    if m > n :
        Functions += [equals for _ in range(m-n)]
    if m > l :
        Thresholds += [0 for _ in range(m-l)]
    for x in Set :
        count = 0
        for i in range(m):
            [attr, value] = Properties[i]
            if Functions[i](x[attr], value) > Thresholds[i] :
                count += 1
        count /= m
        if count > score :
            score = count
    return score
