from copy import deepcopy
from numpy import mean, sqrt
from numpy.random import randint, shuffle
from operator import eq
from fuzzy_queries.static.fuzzy_queries.src.utils import *
# try :
#     from fuzzy_queries.static.fuzzy_queries.src.utils import *
# except :
#     from utils import *

class Dataset(object):
    """Class used to implement concept learning methods, namely CHOCOLATE, nearest neighbors and mean distance."""

    FUNCTIONS = [eq, relative_sim, discrete_sim, discrete_sim, inf_or_relative, eq, eq, eq, relative_sim, relative_sim, relative_sim] # 11 functions to compute the similarity (1 - normalized distance) between all 11 attributes of the current database
    LABELS = ["type", "surface", "pieces", "chambres", "loyer", "meuble", "jardin", "terrasse", "dist_centre", "dist_transport", "dist_commerce"] # attributes labels for the current database
    Data = [] # list of representative data points used to define a fuzzy concept, and its membership function
    Functions = [] # (fuzzy) functions to compute the "distance" between elements
    Thresholds = [] # thresholds used by the CHOCOLATE strategy, to determine if a property is verified or not
    Indices = [] # attributes to consider
    n_attr = 0 # length of Indices


    def __init__(self, Data=[], Functions=[], Thresholds=[], Indices=[]):
        """Initialize the dataset with a 2D table (Data), and lists of (fuzzy) functions and thresholds used to compute fuzzy conditions. If Functions or Thresholds is shorter than the number of attributes of Data, the default condition is strict equality."""
        self.Data = Data
        self.Functions = Functions
        self.Thresholds = Thresholds
        if Data and Data[0] : self.n_attr = len(Data[0])
        self.Indices = Indices if Indices else [k for k in range(self.n_attr)] # All attributes are used if not specified
        lf, lt = len(Functions), len(Thresholds)
        if lf < self.n_attr :
            self.Functions += [eq for _ in range(self.n_attr-lf)] # Default function is eq
        if lt < self.n_attr :
            self.Thresholds += [0 for _ in range(self.n_attr-lt)] # Default threshold is 0



    def add_data_point(self, element):
        """Add a row to Data."""
        self.Data.append(element)



    def remove_data_point(self, index, id=None):
        """Remove one of the data points."""
        if index < len(self.Data) :
            del self.Data[index]
        # elif id :
        #     for d in self.Data :
        #         if d[0] == id :
        #             self.Data.remove(d)
    


    def delta(self, attr, value, function=eq, threshold=0):
        """Measures the proportion of elements in Data (2D array), of which attribute attr satisfies the condition : function(attr, value) > threshold ; i.e. the data points that verify the property [attr, value].
        By default, the condition is strict equality."""
        ret = 0
        for x in self.Data :
            if function(value, x[attr]) > threshold :
                ret += 1
        return ret/len(self.Data)



    def mu(self, Properties, F=[], T=[]):
        """Returns the maximal similarity between an element of Data and Properties (list of [attribute, value] couples).
        The score is 1 if there is x in Data which, for all tuples in Properties, verifies : function(attribute, value) > threshold.
        The functions and thresholds are taken from their respective lists, which must be at least as long as Properties."""
        if not Properties : return 0
        if not F : F = self.Functions
        if not T : T = self.Thresholds
        score = 0
        for x in self.Data : # for each data point
            count = 0
            for i in range(len(Properties)):
                [attr, value] = Properties[i]
                if F[i](value, x[attr]) > T[i] : # count how many properties this data point verifies
                    count += 1
            if count > score : # look for the max number of properties verified by one data point
                score = count
        return score/n_attr



    def choquet(self, x):
        """Returns a measure of how well x satisfies the concept described by the data points in Data (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in Data, as well as the closeness to all data points.
        The functions and thresholds used to evaluate each attribute are taken from their respective lists : the condition is strict equality by default."""

        deltas = []
        for i in range(self.n_attr): # create the list of delta measures for each attribute of x
            deltas.append([self.delta(i, x[i], self.Functions[i], self.Thresholds[i]), i]) # i needs to be tracked for later
        zipped = [list(z) for z in zip(deltas, self.Functions, self.Thresholds)] # associate each delta with the attribute's corresponding function and threshold
        zipped.sort(reverse=True) # sorts the delta measures in descending order

        deltas, F, T = [], [], []
        for z in zipped : # separate the delta measures, functions and thresholds (the three lists are still ordered coherently)
            deltas.append(z[0])
            F.append(z[1])
            T.append(z[2])

        H, G = [], []
        Sc = 0
        for i in range(self.n_attr):
            attr = deltas[i][1] # for each attribute (in descending order)
            G.append([attr, x[attr]]) # i-th most important property according to delta
            Sc += deltas[i][0] * (self.mu(G, F, T) - self.mu(H, F, T)) # Choquet integral ; G (resp. H) is the subset of the i (resp. i-1) most important properties
            H = deepcopy(G)
        return Sc



    def select_above_limit(self, Set, limit):
        """Applies the CHOCOLATE method to each row of Set (2D list), and returns those with a score greater than limit."""
        selection = []
        for entry in Set :
            if self.choquet(entry) >= limit :
                selection.append(entry)
        return selection



    def select_most_satisfying(self, Set, n):
        """Applies the CHOCOLATE method to each row of Set (2D list), and returns the n entries with the highest scores."""
        scores = []
        for entry in Set :
            scores.append([self.choquet(entry)] + entry)
        scores.sort(reverse=True)
        return scores[:n]



    # def Sc_min(self, attr, element):
    #     """Finds the minimal relative distance between element and a data point in Data, taking only one attribute into account."""
    #     dist = []
    #     for x in self.Data:
    #         m = max([x[attr],element[attr]])
    #         if not m:
    #             continue
    #         else:
    #             dist.append(abs(x[attr]-element[attr])/m)
    #     return min(dist)



    def nearest_neighbor(self, element):
        """Returns the relative distance between element and its nearest neighbor in Data.
        Takes into account all of the attributes listed in Indices."""
        dist = []
        for x in self.Data:
            dist.append([])
            for attr in self.Indices :
                dist[-1].append(1-self.Functions[attr](x[attr], element[attr]))
                # dist[-1].append((1-Functions[attr](x[attr], element[attr]))**2)
        mean_dist = []
        for d in dist :
            mean_dist.append(mean(d))
            # mean_dist.append(sqrt(sum(d))/len(indices))
        minimum = min(mean_dist)
        return minimum



    def mean_total_distance(self, element):
        """Returns the average relative distance between element and all data points in Data.
        Takes into account all of the attributes listed in Indices."""
        return mean([self.mean_distance(attr, element) for attr in self.Indices])



    def mean_distance(self, attr, element):
        """Returns the average relative distance between element and all data points in Data, taking only one attribute into account."""
        dist = []
        for x in self.Data :
            dist.append(1-self.Functions[attr](x[attr], element[attr]))
        return mean(dist)



    def user_test_selection(self, Set, n_best, n_worst, n_strange):
        """Applies the three concept learning methods (CHOCOLATE, NN, mean distance) to each row of Set (2D list), and returns for each method the n_best entries with the highest scores, the n_worst entries with the lowest scores, and n_strange randomly selected entries in Data : there are 3*(n_best + n_worst + n_strange) results."""
        scores = []
        best, worst, strange = [], [], []
        for entry in Set :
            scores.append([self.choquet(entry)] + [self.nearest_neighbor(entry)] + [self.mean_total_distance(entry)] + [entry])

        scores.sort(reverse=True)
        best += [["c", "b"] + [s[0]] + s[3] for s in scores[:n_best]]
        worst += [["c", "w"] + [s[0]] + s[3] for s in scores[-n_worst:]]
        scores_left = deepcopy(scores)[n_best:-n_worst]
        for i in range(n_strange):
            r = randint(len(scores_left))
            strange.append(["c", "s"] + [scores_left[r][0]] + scores_left[r][3])
            del scores_left[r]
        for s in scores :
            del s[0]
            
        scores.sort(reverse=True)
        best += [["n", "b"] + [s[0]] + s[2] for s in scores[:n_best]]
        worst += [["n", "w"] + [s[0]] + s[2] for s in scores[-n_worst:]]
        scores_left = deepcopy(scores)[n_best:-n_worst]
        for i in range(n_strange):
            r = randint(len(scores_left))
            strange.append(["n", "s"] + [scores_left[r][0]] + scores_left[r][2])
            del scores_left[r]
        for s in scores :
            del s[0]
            
        scores.sort(reverse=True)
        best += [["d", "b"] + [s[0]] + s[1] for s in scores[:n_best]]
        worst += [["d", "w"] + [s[0]] + s[1] for s in scores[-n_worst:]]
        scores_left = deepcopy(scores)[n_best:-n_worst]
        for i in range(n_strange):
            r = randint(len(scores_left))
            strange.append(["d", "s"] + [scores_left[r][0]] + scores_left[r][1])
            del scores_left[r]

        results = best + worst + strange
        shuffle(results)
        return results



    # def user_test_selection_CHOCOLATE(self, Set, n_best, n_worst, n_strange):
    #     """Applies the CHOCOLATE method to each row of Set (2D list), and returns the n_best entries with the highest scores, the n_worst entries with the lowest scores, and n_strange randomly selected entries in Data."""
    #     scores = []
    #     for entry in Set :
    #         scores.append([self.choquet(entry)] + entry)
    #     scores.sort(reverse=True)
    #     best = scores[:n_best]
    #     worst = scores[-n_worst:]
    #     strange = []
    #     scores_left = scores[n_best:-n_worst]
    #     for i in range(n_strange):
    #         r = randint(len(scores_left))
    #         strange.append(scores_left[r])
    #         del scores_left[r]
    #     return best + strange + worst





class Fuzzy_Dataset(Dataset):
    """Implements another version of CHOCOLATE without thresholds, that instead uses fuzzy functions directly to smooth out the membership function."""

    pass

    def __init__(self, Data=[], Functions=[], Thresholds=[], Indices=[]):
        """Initialize the dataset with a 2D list (Data), and a list of (fuzzy) functions used to compare data. If Functions is shorter than the number of attributes in Data, the default functions are strict equality."""
        self.Data = Data
        self.Functions = Functions
        if Data and Data[0] : self.n_attr = len(Data[0])
        self.Indices = Indices if Indices else [k for k in range(self.n_attr)] # All attributes are used if not specified
        lf = len(Functions)
        if lf < self.n_attr :
            self.Functions += [eq for _ in range(self.n_attr-lf)] # Default function is eq



    def delta(self, attr, value, function=eq):
        """Measures how well value matches the properties in Data.
        By default, the function is strict equality."""
        ret = 0
        for x in self.Data :
            ret += function(value, x[attr])
        return ret/len(self.Data)



    def mu(self, Properties, F=[]):
        """Returns the maximal similarity between an element of Data and Properties (subset of attributes and values).
        The score is 1 if there is x in data which, for all tuples in Properties, verifies : function(value, attribute) == 1.
        The list of functions, if provided, must be at least as long as Properties."""
        if not Properties : return 0
        if not F : F = self.Functions
        score = 0
        m = len(self.Data[0])
        for x in self.Data : # for each data point
            count = 0
            for i in range(len(Properties)):
                [attr, value] = Properties[i]
                count += F[i](value, x[attr]) # count "how much" each property is verified by this data point
            count /= m
            if count > score :
                score = count
        return score



    def choquet(self, x):
        """Returns a measure of how well x satisfies the concept described by the data points in Data (between 0 and 1), based on a Choquet integral. It takes into account the satisfaction of the most important properties in data, as well as the closeness to all data points.
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
