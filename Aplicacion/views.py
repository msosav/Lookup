from pickle import FALSE
from django.http import HttpResponseRedirect
from django.shortcuts import render
from scraping import getMercadoLibre
from Aplicacion.models import Producto
from pymongo import MongoClient

# Se conecta a la base de datos
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["lookup"]
collection = db["Aplicacion_producto"]

# Create your views here.


def inicio(request):
    analiticas = []
    for documentos in collection.find():
        if collection.count_documents({"nombre": documentos["nombre"]}) >= 1:
            if documentos["nombre"].lower() not in analiticas:
                analiticas.append(documentos["nombre"])
    analiticas.sort()
    for elemento in range(0, len(analiticas)):
        analiticas[elemento] = analiticas[elemento].capitalize()
    top_5 = analiticas[0:5]

    imagen = "https://m.media-amazon.com/images/I/613AVx005lL._AC_SX522_.jpg"
    caracteristicas = ["Pantalla Super Retina XDR de 6,1 pulgadas",
                       "El modo Cine añade poca profundidad de campo y cambia el enfoque automáticamente en los vídeos", "Sistema avanzado de cámara dual de 12 Mpx con gran angular y ultra gran angular, Estilos Fotográficos, HDR Inteligente 4, modo Noche y grabación de vídeo en 4K HDR con Dolby Vision"]
    if request.method == 'POST':
        nombre = request.POST.get("producto_buscado").capitalize()
        lista = getMercadoLibre(nombre)
        rating = lista[0]
        precio = lista[1]
        url = lista[2]
        if float(rating) < 4.6:
            recomendado = False
        else:
            recomendado = True
        # Guardar en la base de datos
        p = Producto(nombre=nombre, price=precio,
                     rating=rating, recomendado=recomendado)
        p.save()
        if (recomendado == False):
            return render(request, 'inicio.html', {"productos": top_5, "nombre2": "funciona",
                                                   "valoracion2": rating, "precio2": precio, "portal2": url,
                                                   "imagen2": imagen, "caracteristicas2": caracteristicas, })
        else:
            return render(request, 'inicio.html', {"productos": top_5, "nombre": nombre,
                                                   "valoracion": rating, "precio": precio, "portal": url,
                                                   "imagen": imagen, "caracteristicas": caracteristicas, })
    return render(request, 'inicio.html', {"productos": top_5})


def historial(request):
    return render(request, 'historial.html')


def confirmacion(request):
    return render(request, 'confirmacion.html')
