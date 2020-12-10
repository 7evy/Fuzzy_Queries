from django.db.models.query import QuerySet
from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Fuzzy_Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
# from fuzzy_queries.static.fuzzy_queries.src.clustering import *
# Create your views here.



def index(request):
    request.session['immo_list'] = list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
    real_immo = [request.session['immo_list'][4*k] for k in range(0, len(request.session['immo_list'])//4)]
    C = Clustering(real_immo, Clustering.FUNCTIONS, [k for k in range(1, 12)])
    C.by_affinity(0)
    request.session['suggestions'] = C.centers()
    request.session['max'] = C.n_clusters
    request.session['examples'] = []
    context = {
        'current': request.session['suggestions'][1],
        'pos': 1
    }
    return render(request, 'fuzzy_queries/index.html', context)



def next_suggestion(request, pos, ans):
    if ans :
        request.session['examples'].append(request.session['suggestions'][pos])
    if pos+1 >= request.session['max'] :
        return results(request)
    context = {
        'current': request.session['suggestions'][pos+1],
        'pos': pos+1
    }
    return render(request, 'fuzzy_queries/index.html', context)



def results(request):
    res = []
    immo_list = request.session['immo_list']
    ex = request.session['examples']
    for e in ex :
        e.pop(0)
    for row in immo_list :
        row.pop(0)
    D = Fuzzy_Dataset(ex, Fuzzy_Dataset.FUNCTIONS)
    best = D.select_most_satisfying(immo_list, 10)
    for e in ex :
        e = dict(zip(Fuzzy_Dataset.LABELS, e))
    for b in best :
        b = dict(zip(["score"] + Fuzzy_Dataset.LABELS, b))
    print(best)
    context = {
        'immo': best,
        'examples': ex
    }
    return render(request, 'fuzzy_queries/results.html', context)

