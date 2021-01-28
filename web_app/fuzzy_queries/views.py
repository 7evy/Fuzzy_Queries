from django.db.models.expressions import ExpressionWrapper
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponseRedirect
from fuzzy_queries.models import Immo
from fuzzy_queries.static.fuzzy_queries.src.dataset import Fuzzy_Dataset
from fuzzy_queries.static.fuzzy_queries.src.utils import *
from fuzzy_queries.static.fuzzy_queries.src.clustering import Clustering
from time import time
from numpy import mean
# Create your views here.



def welcome(request):
    return render(request, 'fuzzy_queries/welcome.html')



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



def welcome_2(request):
    context = {
        'examples': request.session['examples']
    }
    return render(request, 'fuzzy_queries/welcome_2.html', context)



def next_suggestion(request, pos, ans):
    if ans :
        request.session['examples'].append(request.session['suggestions'][pos])
    if pos+1 >= request.session['max'] or len(request.session['examples']) >= 5 :
        if not request.session['examples'] :
            return index(request)
        else :
            # return results(request)
            return welcome_2(request)
    context = {
        'current': request.session['suggestions'][pos+1],
        'pos': pos+1,
        'examples': request.session['examples']
    }
    return render(request, 'fuzzy_queries/index.html', context)



def user_test(request):
    res = []
    ex = request.session['examples']
    D = Fuzzy_Dataset(ex, Fuzzy_Dataset.FUNCTIONS)
    for e in ex :
        try :
            request.session['immo_list'].remove(e)
        except ValueError :
            break
    # sel = D.user_test_selection(request.session['immo_list'], 1, 1, 1)
    sel = D.user_test_selection(request.session['immo_list'], 10, 5, 5)
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
    request.session['marks'] = marks
    request.session['global_marks'] = {}
    request.session['global_marks']['best'] = sum(marks[:10])/50
    request.session['global_marks']['strange'] = sum(marks[10:15])/25
    request.session['global_marks']['worst'] = sum(marks[15:])/25
    request.session['individual_marks'] = []
    return HttpResponseRedirect("/fuzzy_queries/welcome_3/")

def welcome_3(request):
    return render(request, "fuzzy_queries/welcome_3.html")

def user_test_inter2(request):
    context = {
        'current': request.session['results'][0],
        'pos': 0,
        'nextpos': 1,
        'examples': request.session['examples']
    }
    return render(request, "fuzzy_queries/user_test_part2.html", context)



def user_test_part2(request, pos, ans):
    request.session['individual_marks'].append(ans.split(";")[1:-1])

    if pos+1 >= 10 :
        request.session['time'] = time() - request.session['time']
        request.session['example_marks'] = [0 for _ in request.session['examples']]
        for l in request.session['individual_marks'] :
            if l :
                for e in l :
                    request.session['example_marks'][int(e)] += 1
        return user_test_results(request)
    context = {
        'current': request.session['results'][pos+1],
        'pos': pos+1,
        'nextpos': pos+2,
        'examples': request.session['examples']
    }
    return render(request, 'fuzzy_queries/user_test_part2.html', context)



def user_test_results(request):
    final_mark = 0
    avg_score = 0
    ttl_score = 0
    context = {}
    for i in range(10) :
        avg_score += request.session['results'][i][0]
        ttl_score += request.session['results'][i][0] * request.session['marks'][i]
    final_mark += ttl_score
    avg_score = int(avg_score*100)/1000
    ttl_score = int(ttl_score*100)/5000
    recap = "Les meilleurs résultats selon CHOCOLATE ont un score moyen de : " + str(avg_score) + "\nLa note moyenne attribuée par l'utilisateur est : " + str(request.session['global_marks']['best']) + "\nScore total : " + str(ttl_score) + "\n"
    context["best_score"] = avg_score
    context["best_mark"] = request.session['global_marks']['best']
    context["best_grade"] = ttl_score
    avg_score = 0
    ttl_score = 0
    for i in range(10, 15) :
        avg_score += request.session['results'][i][0]
        ttl_score += request.session['results'][i][0] * request.session['marks'][i]
    avg_score = int(avg_score*100)/500
    ttl_score = int(ttl_score*100)/2500
    recap += "\nLes résultats aléatoires ont un score moyen de : " + str(avg_score) + "\nLa note moyenne attribuée par l'utilisateur est : " + str(request.session['global_marks']['strange']) + "\nScore total : " + str(ttl_score) + "\n"
    context["rand_score"] = avg_score
    context["rand_mark"] = request.session['global_marks']['strange']
    context["rand_grade"] = ttl_score
    avg_score = 0
    ttl_score = 0
    for i in range(15, 20) :
        avg_score += request.session['results'][i][0]
        ttl_score += request.session['results'][i][0] * request.session['marks'][i]
    final_mark -= ttl_score
    avg_score = int(avg_score*100)/500
    ttl_score = int(ttl_score*100)/2500
    recap += "\nLes pires résultats selon CHOCOLATE ont un score moyen de : " + str(avg_score) + "\nLa note moyenne attribuée par l'utilisateur est : " + str(request.session['global_marks']['worst']) + "\nScore total : " + str(ttl_score) + "\n\n\n"
    context["worst_score"] = avg_score
    context["worst_mark"] = request.session['global_marks']['worst']
    context["worst_grade"] = ttl_score
    for e in range(len(request.session['examples'])):
        recap += "L'exemple n°" + str(e+1) + " est représentatif de " + str(request.session['example_marks'][e]) + " résultats.\n"
    context["ex"] = request.session['example_marks']
    if 0 not in request.session['example_marks'] :
        recap += "Tous les exemples sont pris en compte par les résultats.\n"
    final_mark += sum(request.session['example_marks'])
    m = mean(request.session['example_marks'])
    for e in request.session['example_marks'] :
        final_mark -= abs(e-m)
    final_mark = int((final_mark+30)*10000/130)/100
    recap += "\n\nNote globale : " + str(final_mark) + "/100\nLe test a duré " + str(int(request.session['time']*100)/100) + " s.\n"
    context["global_grade"] = final_mark
    context["time"] = int(request.session['time']*100)/100
    with open('data/user_test.txt', 'w', encoding='utf-8') as f:
        f.write(recap)
    return render(request, 'fuzzy_queries/test_results.html', context)



# def test(request):
#     immo = Immo.objects.all()
#     context = {
#         'immo': immo
#     }
#     return render(request, "fuzzy_queries/test.html",context)



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
