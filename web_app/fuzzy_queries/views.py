from django.db.models.expressions import ExpressionWrapper
from django.db.models.query import QuerySet
from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Fuzzy_Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
from time import time
# Create your views here.



def index(request):
    if 'immo_list' not in request.session :
        request.session['immo_list'] = list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
    for row in request.session['immo_list'] :
        row.pop(0)
    real_immo = [request.session['immo_list'][4*k] for k in range(len(request.session['immo_list'])//4)]
    C = Clustering(real_immo, Clustering.FUNCTIONS)
    C.by_affinity(0.47, 40)
    request.session['suggestions'] = C.centers()
    request.session['max'] = C.n_clusters
    request.session['examples'] = []
    context = {
        'current': request.session['suggestions'][0],
        'pos': 0
    }
    request.session['time'] = time()
    return render(request, 'fuzzy_queries/index.html', context)



def next_suggestion(request, pos, ans):
    if ans :
        request.session['examples'].append(request.session['suggestions'][pos])
    if pos+1 >= request.session['max'] or len(request.session['examples']) >= 5 :
        if not request.session['examples'] :
            return index(request)
        else :
            # return results(request)
            return user_test(request)
    context = {
        'current': request.session['suggestions'][pos+1],
        'pos': pos+1,
        'examples': request.session['examples']
    }
    return render(request, 'fuzzy_queries/index.html', context)



def user_test(request):
    res = []
    immo_list = request.session['immo_list']
    ex = request.session['examples']
    D = Fuzzy_Dataset(ex, Fuzzy_Dataset.FUNCTIONS)
    sel = D.user_test_selection(immo_list, 1, 1, 1) # sel = D.user_test_selection(immo_list, 10, 5, 5)
    # ex2, sel2 = [], []
    # for e in ex :
    #     ex2.append(dict(zip(Fuzzy_Dataset.LABELS, e)))
    # for s in sel :
    #     sel2.append(dict(zip(["score"] + Fuzzy_Dataset.LABELS, s)))
    request.session['results'] = sel
    context = {
        'immo': sel,
        'examples': ex,
        'length': len(sel)
    }
    return render(request, 'fuzzy_queries/user_test.html', context)



def user_test_inter(request, str_marks):
    marks = []
    for m in str_marks.split(";")[:-1] :
        marks.append(int(m))
    request.session['global_marks'] = {}
    request.session['global_marks']['best'] = sum(marks[:10])/50
    request.session['global_marks']['strange'] = sum(marks[10:15])/25
    request.session['global_marks']['worst'] = sum(marks[15:])/25
    request.session['individual_marks'] = []
    print(request.session['results'][0])
    context = {
        'current': request.session['results'][0],
        'pos': 0,
        'examples': request.session['examples']
    }
    return render(request, "fuzzy_queries/user_test_part2.html", context)



def user_test_part2(request, pos, ans):
    request.session['individual_marks'].append(ans.split(";"))
    print(request.session['individual_marks'])
    if pos+1 >= len(request.session['results']) :
        request.session['time'] = time() - request.session['time']
        return None
    context = {
        'current': request.session['results'][pos+1],
        'pos': pos+1,
        'examples': request.session['examples']
    }
    return render(request, 'fuzzy_queries/user_test_part2.html', context)



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
