from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def historial(request):
    return render(request, 'historial.html')