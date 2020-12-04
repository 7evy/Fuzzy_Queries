from django.db.models.query import QuerySet
from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
# from fuzzy_queries.static.fuzzy_queries.src.clustering import *
# Create your views here.


def index(request):
    # immo = Immo.objects.all()
    immo_list = list([list(Immo.objects.values()[k].values()) for k in range(len(Immo.objects.all()))])
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
    return render(request, 'fuzzy_queries/index.html', context)

    

# def index(request):
#     immo = list(Immo.objects.values().values())
#     real_immo = [immo[4*k] for k in range(0, len(immo)//4)]
#     suggestions = Clustering(immo, Clustering.FUNCTIONS)
#     context = {
#         'suggestions': suggestions
#     }
#     return render(request, 'fuzzy_queries/index.html', context)

# def results(request):
#     immo = Immo.objects.all()
#     message = msg()
#     context = {
#         'immo': immo,
#         'msg': message
#     }
#     return render(request, 'fuzzy_queries/index.html', context)