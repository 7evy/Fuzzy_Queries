from copy import deepcopy
from choquet import equals


class Dataset(set):

    data = []

    def __init__(self, data=[]):
        self.data = data

    def add_example(self, example):
        data.append(example)

    def remove_example(self, index=None, id=None):
        if index :
            data.pop(index)
        elif id :
            for d in data :
                if d[0] == id :
                    data.remove(d)
    
    def delta(self, attr, value, function=equals, threshold=0):
        """Measures the proportion of elements in data (2D array), of which attribute attr satisfies the condition : function(attr, value) > threshold.
        By default, the condition is strict equality."""
        ret = 0
        for x in self.data :
            if function(x[attr], value) > threshold :
                ret += 1
        return ret/len(self.data)

    def mu(self, Properties, Functions=[], Thresholds=[]):
        """Returns the maximal similarity between an element of data (2D array) and Properties (subset of attributes and values).
        The score is 1 if there is x in data which, for all tuples in Properties, verifies : function(attribute, value) > threshold.
        The functions and thresholds are taken from their respective lists, which must be at least as long as Properties."""
        if not Properties : return 0
        score = 0
        m = len(self.data[0])
        for x in self.data :
            count = 0
            for i in range(len(Properties)):
                [attr, value] = Properties[i]
                if Functions[i](x[attr], value) > Thresholds[i] :
                    count += 1
            count /= m
            if count > score :
                score = count
        return score

    def choquet(self, x, Functions=[], Thresholds=[]):
        """Returns a measure of how well x satisfies the concept described by the examples in data (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in data, as well as the closeness to all examples.
        The functions and thresholds used to evaluate each attribute are taken from their respective lists : the condition is strict equality by default."""
        l, f, t = len(x), len(Functions), len(Thresholds)
        if l > f :
            Functions += [equals for _ in range(l-f)]
        if l > t :
            Thresholds += [0 for _ in range(l-t)]

        deltas = []
        for i in range(l):
            deltas.append([delta(self.data, i, x[i], Functions[i], Thresholds[i]), i])
        deltas.sort(reverse=True)

        H, G = [], []
        Sc = 0
        for i in range(l):
            attr = deltas[i][1]
            G.append([attr, x[attr]])
            Sc += deltas[i][0] * (mu(self.data, G, Functions, Thresholds) - mu(self.data, H, Functions, Thresholds))
            H = deepcopy(G)
        return Sc
