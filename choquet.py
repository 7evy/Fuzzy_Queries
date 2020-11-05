from copy import deepcopy
from numpy import mean


Test = [["BC1", "P", 1, 0, "A+"],
        ["PHD", "M", 1, 0, "B+"],
        ["BC3", "A", 0, 0, "A+"],
        ["BC3", "I", 1, 0, "A-"],
        ["MASTER", "B", 1, 0, "A+"]]

# Test = [["Appartement",45.1,2,1,621,"non","non","non",1689,820,2126]
#         ["Appartement",91.2,5,4,1824,"oui","non","non",60,22,1145]
#         ["Maison",90.5,5,4,788,"non","oui","non",991,361,122]
#         ["Maison",112.2,5,3,1020,"oui","non","non",3279,853,2950]
#         ["Appartement",42.6,2,1,414,"non","non","non",3745,1146,2919]
#         ["Studio",27.7,2,1,294,"oui","non","oui",836,426,2588]
#         ["Studio",26.3,1,1,341,"oui","non","non",2004,1444,4499]
#         ["Appartement",82.0,3,2,676,"oui","non","non",2964,1307,250]
#         ["Appartement",77.7,3,2,634,"oui","non","non",3443,805,3684]
#         ["Appartement",42.6,2,1,425,"oui","non","non",2639,1268,2329]]

def Sc_min(Set, attr, value):
    dist = []
    for x in Set:
        m = max([x[attr],value[attr]])
        if not m:
            continue
        else:
            dist.append(abs(x[attr]-value[attr])/m)
    return min(dist)

def Sc_avg(Set, attr, value):
    dist = []
    for x in Set:
        m = max([x[attr],value[attr]])
        if not m:
            continue
        else:
            dist.append(abs(x[attr]-value[attr])/m)
    return mean(dist)
        
  

def equals(a, b):  # Default function
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
    """Returns a measure of how well x satisfies the concept described by Set (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in Set, as well as the closeness to all examples.
    The functions and thresholds used to evaluate each attribute are taken from their respective lists : the condition is strict equality by default."""
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
        Sc += deltas[i][0] * (mu(Set, G, Functions, Thresholds) - mu(Set, H, Functions, Thresholds))
        H = deepcopy(G)
    return Sc

def relative_distance(x, y):
    return abs(x-y)/max(x, y)

def relative_sim(x, y):
    return 1 - relative_distance(x, y)
        
print(choquet(Test, ["BC3", "A", 0, 0, "A+"])) # Should return exactly 0.48 (?)
print(choquet(Test, ["PHD", "L", 1, 0, "B-"]))
