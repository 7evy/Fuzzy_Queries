from django.shortcuts import render
from fuzzy_queries.models import Immo

# Create your views here.

def index(request):
    immo = Immo.objects.all()
    context = {
        'immo': immo
    }
    return render(request, 'fuzzy_queries/index.html', context)