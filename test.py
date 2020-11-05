from dataset import Dataset
import time


indices = [1,2,3,4,8,9,10]

def equals(x, y):  # Default function
    return x == y

def relative_distance(x, y):
    return 0 if x == y else abs(x-y)/max(x, y)

def relative_sim(x, y):
    return 1 - relative_distance(x, y)

def inf_or_relative(x, y):
    return 1 if x <= y else relative_sim(x, y)

Test_subset = [["Appartement",45.1,2,1,621,0,0,0,1689,820,2126],
        ["Appartement",91.2,5,4,1824,1,0,0,60,22,1145],
        ["Maison",90.5,5,4,788,0,1,0,991,361,122],
        ["Maison",112.2,5,3,1020,1,0,0,3279,853,2950],
        ["Appartement",42.6,2,1,414,0,0,0,3745,1146,2919],
        ["Studio",27.7,2,1,294,1,0,1,836,426,2588],
        ["Studio",26.3,1,1,341,1,0,0,2004,1444,4499],
        ["Appartement",82.0,3,2,676,1,0,0,2964,1307,250],
        ["Appartement",77.7,3,2,634,1,0,0,3443,805,3684],
        ["Appartement",42.6,2,1,425,1,0,0,2639,1268,2329]]

Test_entry = ["Appartement", 50.0, 3, 1, 500, 1, 0, 1, 100, 2000, 1000]

Test_bdd = [["Studio",17.98,1,1,440,1,0,0,727,575,3708],
["Studio",18.6,1,1,450,1,0,0,818,366,308],
["Studio",16.6,1,1,470,1,0,0,613,145,111],
["Studio",17.7,1,1,465,1,0,0,2046,345,378],
["Appartement",62.0,2,2,400,1,0,0,3922,1910,1056],
["Appartement",64.5,2,2,409,1,0,0,3646,1378,512],
["Appartement",65.4,2,2,408,1,0,0,3521,491,1808],
["Appartement",58.26,3,2,709,0,0,1,275,144,1585],
["Appartement",58.6,3,2,731,0,0,1,1802,800,7],
["Appartement",55.1,3,2,664,0,0,1,708,91,1653],
["Appartement",41.5,2,1,580,0,0,0,1480,119,488],
["Appartement",39.1,2,1,602,0,0,0,1328,528,1975],
["Appartement",42.2,2,1,614,0,0,0,973,34,145],
["Appartement",38.5,2,1,539,0,0,0,907,137,3962],
["Appartement",48.0,2,1,592,0,0,0,482,86,2413],
["Appartement",51.3,2,1,596,0,0,0,1660,67,45],
["Appartement",47.1,2,1,588,0,0,0,2636,46,1294],
["Appartement",51.4,2,1,647,0,0,0,835,951,1395],
["Appartement",70.9,3,2,785,0,0,1,2083,429,4667],
["Appartement",72.0,4,3,854,1,0,0,570,225,3968],
["Appartement",30.0,2,1,490,1,0,0,1706,885,70],
["Appartement",30.1,2,1,462,1,0,0,762,707,424],
["Appartement",30.0,2,1,467,1,0,0,2180,1801,1711],
["Appartement",31.1,2,1,479,1,0,0,1626,558,2681],
["Appartement",66.0,3,2,790,1,0,0,3715,894,642],
["Appartement",64.5,3,2,776,1,0,0,3648,1673,3054],
["Appartement",69.2,3,2,791,1,0,0,2093,479,3843]]

D = Dataset(Test_subset)

# print(D.choquet(Test_entry, [equals, relative_sim, equals, equals, inf_or_relative, equals, equals, equals, relative_sim, inf_or_relative, inf_or_relative], [0, 0.75, 0, 0, 0.75, 0, 0, 0, 0.75, 0.75, 0.75]))

# start_time = time.time()
# print(D.select_most_satisfying(Test_bdd, 0.5, [equals, relative_sim, equals, equals, inf_or_relative, equals, equals, equals, relative_sim, inf_or_relative, inf_or_relative], [0, 0.75, 0, 0, 0.75, 0, 0, 0, 0.75, 0.75, 0.75]))
# print(len(Test_bdd))
# print(time.time()-start_time)

# print(D.mean_total_distance(indices, ["Appartement",69.2,3,2,791,1,0,0,2093,479,3843]))
print(D.nearest_neighbor(indices, ["Appartement",69.2,3,2,791,1,0,0,2093,479,3843]))






