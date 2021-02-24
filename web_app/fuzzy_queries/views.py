from django.db.models.expressions import ExpressionWrapper
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect
from web_app.settings import ALLOWED_HOSTS
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Dataset, Fuzzy_Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
from time import time
from numpy import mean


SKIP_TEST = False # Debug constant to skip most of the test



def welcome(request): # home page
    return render(request, 'fuzzy_queries/welcome.html')



def index(request, str_indices): # start example selection
    if 'immo_list' not in request.session : # load the database
        immo_list = list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
        for row in immo_list : # Remove serial IDs
            row.pop(0)

    # compute clusters for example selection
    real_immo = [immo_list[4*k] for k in range(len(immo_list)//4)] # 625 real entries in the database
    C = Clustering(real_immo, Clustering.FUNCTIONS)
    C.by_affinity(0.47, 40) # affinity clustering with 37 to 43 clusters
    request.session['suggestions'] = C.centers()
    request.session['max'] = C.n_clusters
    
    # store the attributes numbers specified by the user on the home page (all by default)
    indices = []
    for i in str_indices.split(";")[:-1] :
        indices.append(int(i))

    # store the database and indices
    request.session['immo_list'] = immo_list
    request.session['indices'] = indices
    request.session['examples'] = []
    request.session['pos'] = 0
    context = {
        'current': request.session['suggestions'][0],
    }
    request.session['time'] = time()
    return render(request, 'fuzzy_queries/index.html', context)



def next_suggestion(request, ans): # manage example selection
    pos = request.session['pos']
    examples = request.session['examples']
    suggestions = request.session['suggestions']
    if ans :
        examples.append(suggestions[pos])

    # 5 examples chosen or no more to choose from
    if pos+1 >= request.session['max'] or len(examples) >= 5 :
        if not examples : # 0 example chosen
            return index(request)
        else : # at least 1 example
            return welcome_2(request)
    context = {
        'current': suggestions[pos+1],
        'examples': examples
    }
    request.session['pos'] = pos+1
    return render(request, 'fuzzy_queries/index.html', context)



def welcome_2(request): # pre-test page, define the number and proportions of results
    context = {
        'examples': request.session['examples']
    }
    request.session['res_number'] = [60, 10, 5, 5] # 60 results, with the 10 best results, 5 worst and 5 random for each strategy
    return render(request, 'fuzzy_queries/welcome_2.html', context)



def user_test(request): # starts user test
    res = []
    examples = request.session['examples']
    res_number = request.session['res_number']
    immo_list = request.session['immo_list']

    # use one of two CHOCOLATE implementations
    D = Fuzzy_Dataset(examples, Fuzzy_Dataset.FUNCTIONS, [], request.session['indices'])
    # D = Dataset(examples, Dataset.FUNCTIONS, [0.5 for _ in range(11)], request.session['indices'])

    # remove duplicates (examples will not show up in results)
    for e in examples :
        try :
            immo_list.remove(e)
        except ValueError :
            break

    # compute the test results for the CHOCOLATE, nearest neighbor and mean distance strategies
    sel = D.user_test_selection(immo_list, res_number[1], res_number[2], res_number[3])
    request.session['results'] = [sel[i:i+5] for i in range(0, res_number[0]-4, 5)] # slice the results in groups of 5
    request.session['marks'] = [] # will contain user marks
    request.session['pos'] = 0
    context = {
        'immo': request.session['results'][0],
        'examples': examples
    }
    return render(request, 'fuzzy_queries/user_test.html', context)



def next_results(request, str_marks): # manage user test
    pos = request.session['pos']
    res_number = request.session['res_number']
    marks = request.session['marks']
    if SKIP_TEST : # Debug
        print("SKIP TEST")
        marks = [5 for _ in range(res_number[0])]
        return user_test_inter(request)

    # read user marks
    for m in str_marks.split(";")[:-1] :
        marks.append(int(m))

    # test end
    if pos+1 >= res_number/5 : 
        return user_test_inter(request)

    context = {
        'immo': request.session['results'][pos+1],
        'examples': request.session['examples']
    }
    request.session['pos'] = pos+1
    return render(request, 'fuzzy_queries/user_test.html', context)



def user_test_inter(request): # manage test results
    marks = request.session['marks']
    results = request.session['results']
    res_number = request.session['res_number']
    global_marks = {}
    global_marks['chocolate'] = {}
    global_marks['neighbors'] = {}
    global_marks['distance'] = {}
    for method in global_marks :
        global_marks[method]['best'] = 0
        global_marks[method]['worst'] = 0
        global_marks[method]['strange'] = 0

    # parse results
    results = [r[k] for r in results for k in range(5)]
    for i in range(res_number[0]):
        r = results[i]
        if r[0] == "c" :
            method = 'chocolate'
        elif r[0] == "n" :
            method = 'neighbors'
        else :
            method = 'distance'
        if r[1] == "b" :
            place = 'best'
        elif r[1] == "w" :
            place = 'worst'
        else :
            place = 'strange'
        global_marks[method][place] += marks[i]/5 * r[2] # user mark * algorithm mark
    for method in global_marks : # average of marks for every category with each method
        global_marks[method]['best'] /= res_number[1]
        global_marks[method]['worst'] /= res_number[2]
        global_marks[method]['strange'] /= res_number[3]
    fichier = open("data/stats.csv","a",encoding="utf-8")
    new_stats = "Type,Prix,Pièces,Chambres,Loyer,Meublé,Jardin,Terrasse,Centre_Ville,Transports,Commerces\n"

    # write whether each attribute was used or not
    for i in range(11):
        if i in request.session['indices'] :
            new_stats += "Oui"
        else :
            new_stats += "Non"
        new_stats += ","
    new_stats += "\n"

    # write examples
    for apps in request.session['examples']:
        for atts in apps:
            new_stats += str(atts) + ","
        new_stats += "\n"

    # write marks for each strategy
    new_stats += "Method,Best,Worst,Strange\n"
    for method in global_marks:
        new_stats += method + ","
        for place in global_marks[method] :
            new_stats += str(global_marks[method][place]) + ","
        new_stats += "\n"
    fichier.write(new_stats+"\n")
    fichier.close()
    return HttpResponseRedirect("/fuzzy_queries/test_end/")



def user_test_end(request): # user test end
    return render(request, 'fuzzy_queries/test_end.html')



# def user_test_part2(request, pos, ans):
#     request.session['individual_marks'].append(ans.split(";")[1:-1])

#     if pos+1 >= 10 :
#         request.session['time'] = time() - request.session['time']
#         request.session['example_marks'] = [0 for _ in request.session['examples']]
#         for l in request.session['individual_marks'] :
#             if l :
#                 for e in l :
#                     request.session['example_marks'][int(e)] += 1
#         return user_test_results(request)
#     context = {
#         'current': request.session['results'][pos+1],
#         'pos': pos+1,
#         'nextpos': pos+2,
#         'examples': request.session['examples']
#     }
#     return render(request, 'fuzzy_queries/user_test_part2.html', context)



# def results(request):
#     res = []
#     immo_list = request.session['immo_list']
#     ex = request.session['examples']
#     D = Fuzzy_Dataset(ex, Fuzzy_Dataset.FUNCTIONS)
#     best = D.select_most_satisfying(immo_list, 10)
#     ex2, best2 = [], []
#     for e in ex :
#         ex2.append(dict(zip(Fuzzy_Dataset.LABELS, e)))
#     for b in best :
#         best2.append(dict(zip(["score"] + Fuzzy_Dataset.LABELS, b)))
#     context = {
#         'immo': best2,
#         'examples': ex2
#     }
#     return render(request, 'fuzzy_queries/results.html', context)
