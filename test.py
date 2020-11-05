from dataset import Dataset


def equals(x, y):  # Default function
    return x == y

def relative_distance(x, y):
    return abs(x-y)/max(x, y)

def relative_sim(x, y):
    return 1 - relative_distance(x, y)

def inf_or_relative(x, y):
    return 1 if x <= y else relative_sim(x, y)

Test_subset = [["Appartement",45.1,2,1,621,"non","non","non",1689,820,2126],
        ["Appartement",91.2,5,4,1824,"oui","non","non",60,22,1145],
        ["Maison",90.5,5,4,788,"non","oui","non",991,361,122],
        ["Maison",112.2,5,3,1020,"oui","non","non",3279,853,2950],
        ["Appartement",42.6,2,1,414,"non","non","non",3745,1146,2919],
        ["Studio",27.7,2,1,294,"oui","non","oui",836,426,2588],
        ["Studio",26.3,1,1,341,"oui","non","non",2004,1444,4499],
        ["Appartement",82.0,3,2,676,"oui","non","non",2964,1307,250],
        ["Appartement",77.7,3,2,634,"oui","non","non",3443,805,3684],
        ["Appartement",42.6,2,1,425,"oui","non","non",2639,1268,2329]]

Test_entry = ["Appartement", 50.0, 3, 1, 500, "oui", "non", "oui", 100, 2000, 1000]

D = Dataset(Test_subset)

print(D.choquet(Test_entry, [equals, relative_sim, equals, equals, inf_or_relative, equals, equals, equals, relative_sim, inf_or_relative, inf_or_relative], [0, 0.75, 0, 0, 0.75, 0, 0, 0, 0.75, 0.75, 0.75]))
