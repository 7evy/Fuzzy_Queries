from copy import deepcopy


Test = [["BC1", "PH", 1, 0, "A+"],
        ["PHD", "M", 1, 0, "B+"],
        ["BC3", "A", 0, 0, "A+"],
        ["BC3", "I", 1, 0, "A-"],
        ["MASTER", "B", 1, 0, "A+"]]

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
    if not Properties : return 0
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

def choquet(Set, x, Functions=[], Thresholds=[]):


    l, m = len(x), len(Set)
    Functions = [equals for _ in range(l)]
    Thresholds = [0 for _ in range(l)]
    attr_values = [list(set([Set[i][j] for i in range(m)])) for j in range(l)]
    deltas = [[] for _ in range(l)]
    for i in range(l):
        for j in range(len(attr_values[i])):
            print(attr_values[i])
            print(attr_values[i][j])
            deltas[i].append(delta(Set, i, attr_values[i][j], Functions[i], Thresholds[i]))
    
    deltas_max = []
    for i in range(l):
        d = deltas[i].index(max(deltas[i]))
        deltas_max.append([deltas[i][d], d])
    deltas_max.sort(reverse=True)

    H, G = [], []
    Sc=0
    for i in range(l):
        attr = deltas_max[i][1]
        G.append([attr, attr_values[i][attr]])
        Sc += delta(Set, attr, x[attr]) * (mu(Set, G)-mu(Set, H))
        H = deepcopy(G)
    return Sc
        
print(choquet(Test, ["PHD", "L", 1, 0, "B-"]))
