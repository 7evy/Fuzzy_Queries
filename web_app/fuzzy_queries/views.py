from django.db.models.query import QuerySet
from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
# from fuzzy_queries.static.fuzzy_queries.src.clustering import *
# Create your views here.



def index(request):
    immo_list = list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
    real_immo = [immo_list[4*k] for k in range(0, len(immo_list)//4)]
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
    print(request.session['max'])
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
    # immo = Immo.objects.all()
    immo_list = [[]]#list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
    sel, best = random_selection(immo_list, 10)
    examples = []
    for b in sel :
        examples.append(dict({"type":b[1], "surface":b[2], "pieces":b[3], "chambres":b[4], "loyer":b[5], "meuble":b[6],
            "jardin":b[7], "terrasse":b[8], "dist_centre":b[9], "dist_transport":b[10], "dist_commerce":b[11]}))
    immo = []
    for b in best :
        immo.append(dict({"type":b[1][1], "surface":b[1][2], "pieces":b[1][3], "chambres":b[1][4], "loyer":b[1][5], "meuble":b[1][6],
            "jardin":b[1][7], "terrasse":b[1][8], "dist_centre":b[1][9], "dist_transport":b[1][10], "dist_commerce":b[1][11], "score":b[0]}))
    context = {
        'immo': immo,
        'examples': examples
    }
    return render(request, 'fuzzy_queries/results.html', context)

