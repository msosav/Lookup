from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def inicio(request):
    productos = ["Mac", "IPhone 13", "Jordan Retro XI"]
    if request.method == 'POST':
        return HttpResponseRedirect('confirmacion/')
    return render(request, 'inicio.html', {"productos":productos})

def historial(request):
    return render(request, 'historial.html')

def confirmacion(request):
    return render(request, 'confirmacion.html')