from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.test import msg
from fuzzy_queries.static.fuzzy_queries.src.dataset import Dataset
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
# from fuzzy_queries.static.fuzzy_queries.src.clustering import *
# Create your views here.

def index(request):
    immo = Immo.objects.all()
    message = msg()
    context = {
        'immo': immo,
        'msg': message
    }
    return render(request, 'fuzzy_queries/index.html', context)

    

# def index(request):
#     immo = list(Immo.objects.values().values())
#     real_immo = [immo[4*k] for k in range(0, len(immo)//4)]
#     suggestions = Clustering(immo, Immo.FUNCTIONS_CLUSTER)
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