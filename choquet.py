from copy import deepcopy


Test = [["BC1", "PH", 1, 0, "A+"],
        ["PHD", "M", 1, 0, "B+"],
        ["BC3", "A", 0, 0, "A+"],
        ["BC3", "I", 1, 0, "A-"],
        ["MASTER", "B", 1, 0, "A+"]]

def equals(a, b) :  # Default function
    return a == b

def grade_scale(a, b):  # Fuzzy function example
    grades = dict({("A+", 1), ("A", 0.9), ("A-", 0.8), ("B+", 0.7), ("B", 0.6), ("B-", 0.5), ("C+", 0.4), ("C", 0.3), ("C-", 0.2), ("D+", 0.1)})
    diff = 1 - 2*abs(grades.get(a, 0)-grades.get(b, 0))
    return 0 if diff < 0 else diff

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
    The functions and thresholds are taken from their respective lists, which must be at least as long as Properties."""
    if not Properties : return 0
    score = 0
    m = len(Set[0])
    for x in Set :
        count = 0
        for i in range(len(Properties)):
            [attr, value] = Properties[i]
            if Functions[i](x[attr], value) > Thresholds[i] :
                count += 1
        count /= m
        if count > score :
            score = count
    return score

def choquet(Set, x, Functions=[], Thresholds=[]):
    l, f, t = len(x), len(Functions), len(Thresholds)
    if l > f :
        Functions += [equals for _ in range(l-f)]
    if l > t :
        Thresholds += [0 for _ in range(l-t)]

    deltas = []
    for i in range(l):
        deltas.append([delta(Set, i, x[i], Functions[i], Thresholds[i]), i])
    deltas.sort(reverse=True)

    H, G = [], []
    Sc = 0
    for i in range(l):
        attr = deltas[i][1]
        G.append([attr, x[attr]])
        Sc += deltas[i][0] * (mu(Set, G, Functions, Thresholds)-mu(Set, H, Functions, Thresholds))
        H = deepcopy(G)
    return Sc
        
print(choquet(Test, ["BC3", "A", 0, 0, "A+"]))
