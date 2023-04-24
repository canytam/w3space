from django.shortcuts import render
from data.utilities import update_context

# Create your views here.
def p1(request):
    context = {}
    return render(request, 'p1.html', update_context(context))

def p2(request):
    context = {}
    return render(request, 'p2.html', update_context(context))

def about(request):
    context = {}
    return render(request, 'about.html', update_context(context))

def package(request):
    context = {}
    return render(request, 'package2.html', update_context(context))