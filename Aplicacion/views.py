from django.shortcuts import render

# Create your views here.
def inicio(request):
    productos = ["Mac", "IPhone 13", "Jordan Retro XI"]
    return render(request, 'inicio.html', {"productos":productos})

def historial(request):
    return render(request, 'historial.html')