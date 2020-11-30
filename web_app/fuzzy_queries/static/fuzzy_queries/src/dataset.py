from copy import deepcopy
from numpy import mean, sqrt
from operator import eq



class Dataset(object):

    n_attr = 0
    Data = []
    Functions = []
    Thresholds = []


    def __init__(self, Data=[], Functions=[], Thresholds=[]):
        """Initialize the dataset with a 2D table (Data), and lists of (fuzzy) functions and thresholds used to compute fuzzy conditions. If Functions or Thresholds is shorter than the number of attributes of Data, the default condition is strict equality."""
        self.Data = Data
        self.Functions = Functions
        self.Thresholds = Thresholds
        if Data[0] : self.n_attr = len(Data[0])
        lf, lt = len(Functions), len(Thresholds)
        if lf < self.n_attr :
            self.Functions += [eq for _ in range(self.n_attr-lf)]
        if lt < self.n_attr :
            self.Thresholds += [0 for _ in range(self.n_attr-lt)]



    def add_example(self, example):
        """Add a row to Data."""
        self.Data.append(example)



    def remove_example(self, index, id=None):
        """Remove one of the data points."""
        if index < len(Data) :
            self.Data.pop(index)
        # elif id :
        #     for d in self.Data :
        #         if d[0] == id :
        #             self.Data.remove(d)
    


    def delta(self, attr, value, function=eq, threshold=0):
        """Measures the proportion of elements in Data (2D array), of which attribute attr satisfies the condition : function(attr, value) > threshold.
        By default, the condition is strict equality."""
        ret = 0
        for x in self.Data :
            if function(value, x[attr]) > threshold :
                ret += 1
        return ret/len(self.Data)



    def mu(self, Properties, F=[], T=[]):
        """Returns the maximal similarity between an element of Data and Properties (subset of attributes and values).
        The score is 1 if there is x in data which, for all tuples in Properties, verifies : function(attribute, value) > threshold.
        The functions and thresholds are taken from their respective lists, which must be at least as long as Properties."""
        if not Properties : return 0
        if not F : F = self.Functions
        if not T : T = self.Thresholds
        score = 0
        m = len(self.Data[0])
        for x in self.Data :
            count = 0
            for i in range(len(Properties)):
                [attr, value] = Properties[i]
                if F[i](value, x[attr]) > T[i] :
                    count += 1
            count /= m
            if count > score :
                score = count
        return score



    def choquet(self, x):
        """Returns a measure of how well x satisfies the concept described by the examples in data (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in data, as well as the closeness to all examples.
        The functions and thresholds used to evaluate each attribute are taken from their respective lists : the condition is strict equality by default."""

        deltas = []
        for i in range(self.n_attr):
            deltas.append([self.delta(i, x[i], self.Functions[i], self.Thresholds[i]), i])
        zipped = [list(z) for z in zip(deltas, self.Functions, self.Thresholds)]
        zipped.sort(reverse=True)

        deltas, F, T = [], [], []
        for z in zipped :
            deltas.append(z[0])
            F.append(z[1])
            T.append(z[2])

        H, G = [], []
        Sc = 0
        for i in range(self.n_attr):
            attr = deltas[i][1]
            G.append([attr, x[attr]])
            Sc += deltas[i][0] * (self.mu(G, F, T) - self.mu(H, F, T))
            H = deepcopy(G)
        return Sc



    def select_above_limit(self, Set, limit):
        """Applies the CHOCOLATE method to each row of Set (2D table), and returns those with a score greater than limit."""
        selection = []
        for entry in Set :
            if self.choquet(entry) >= limit :
                selection.append(entry)
        return selection



    def select_most_satisfying(self, Set, n):
        """Applies the CHOCOLATE method to each row of Set (2D table), and returns the n entries with the highest scores."""
        scores = []
        for entry in Set :
            scores.append([self.choquet(entry), entry])
        scores.sort(reverse=True)
        return scores[:n]



    def Sc_min(self, attr, element):
        """Finds the minimal relative distance between element and a data point in Data, taking only one attribute into account."""
        dist = []
        for x in self.Data:
            m = max([x[attr],element[attr]])
            if not m:
                continue
            else:
                dist.append(abs(x[attr]-element[attr])/m)
        return min(dist)



    def nearest_neighbor(self, indices, element):
        """Returns the nearest neighbor of element in Data and their relative distance.
        Takes into account all of the attributes listed in indices."""
        dist = []
        for x in self.Data:
            dist.append([])
            for attr in indices :
                m = max([x[attr],element[attr]])
                if not m:
                    dist[-1].append(0)
                else:
                    dist[-1].append((abs(x[attr]-element[attr])/m)**2)
        mean_dist = []
        for d in dist :
            mean_dist.append(sqrt(sum(d))/len(indices))
        minimum = min(mean_dist)
        return mean_dist.index(minimum), minimum



    def mean_total_distance(self, indices, element):
        """Returns the average relative distance between element and all data points in Data.
        Takes into account all of the attributes listed in indices."""
        return mean([self.Sc_avg(attr, element) for attr in indices])



    def Sc_avg(self, attr, element):
        """Returns the average relative distance between element and all data points in Data, taking only one attribute into account."""
        dist = []
        for x in self.Data :
            m = max([x[attr],element[attr]])
            if not m:
                continue
            else:
                dist.append(abs(x[attr]-element[attr])/m)
        return mean(dist)



class Fuzzy_Dataset(Dataset):

    pass

    def __init__(self, Data=[], Functions=[], Thresholds=[]):
        """Initialize the dataset with a 2D table (Data), and a list of (fuzzy) functions used to compare data. If Functions is shorter than the number of attributes of Data, the default functions are strict equality."""
        self.Data = Data
        self.Functions = Functions
        if Data[0] : self.n_attr = len(Data[0])
        lf = len(Functions)
        if lf < self.n_attr :
            self.Functions += [eq for _ in range(self.n_attr-lf)]



    def delta(self, attr, value, function=eq):
        """Measures how well value matches the properties in Data.
        By default, the function is strict equality."""
        ret = 0
        for x in self.Data :
            ret += function(value, x[attr])
        return ret/len(self.Data)



    def mu(self, Properties, F=[]):
        """Returns the maximal similarity between an element of data (2D array) and Properties (subset of attributes and values).
        The score is 1 if there is x in data which, for all tuples in Properties, verifies : function(value, attribute) == 1.
        The list of functions, if provided, must be at least as long as Properties."""
        if not Properties : return 0
        if not F : F = self.Functions
        score = 0
        m = len(self.Data[0])
        for x in self.Data :
            count = 0
            for i in range(len(Properties)):
                [attr, value] = Properties[i]
                count += F[i](value, x[attr])
            count /= m
            if count > score :
                score = count
        return score



    def choquet(self, x):
        """Returns a measure of how well x satisfies the concept described by the examples in Data (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in data, as well as the closeness to all examples.
        The fuzzy functions used for the delta and mu measures are strict equality by default."""

        deltas = []
        for i in range(self.n_attr):
            deltas.append([self.delta(i, x[i], self.Functions[i]), i])
        zipped = [list(z) for z in zip(deltas, self.Functions)]
        zipped.sort(reverse=True)

        deltas, F = [], []
        for z in zipped :
            deltas.append(z[0])
            F.append(z[1])

        H, G = [], []
        Sc = 0
        for i in range(self.n_attr):
            attr = deltas[i][1]
            G.append([attr, x[attr]])
            Sc += deltas[i][0] * (self.mu(G, F) - self.mu(H, F))
            H = deepcopy(G)
        return Sc
