from django.shortcuts import render
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.test import msg
from fuzzy_queries.static.fuzzy_queries.src.dataset import Dataset
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