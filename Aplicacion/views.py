from django.shortcuts import render
from scraping import webScrapping
from Aplicacion.models import Producto
from pymongo import MongoClient
from funciones import analiticas, buscarProducto, informacionDElProducto, categoriaDelProducto, recomendarProducto

# Se conecta a la base de datos
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["lookup"]
collection = db["Aplicacion_producto"]

# Create your views here.

# Variables globales
top5 = analiticas()
categorias = ["Electronicos", "Electrodomesticos", "Hogar"]
imagen = "https://m.media-amazon.com/images/I/613AVx005lL._AC_SX522_.jpg"


def inicio(request):
    global top5, categorias
    return render(request, 'inicio.html', {"productos": top5, "categorias": categorias})


def historial(request):
    return render(request, 'historial.html')


def productoBuscado(request):
    global top5, categorias, imagen, caracteristicas
    if request.method == 'POST':
        nombre = request.POST.get("producto_buscado").capitalize()
        if buscarProducto(nombre) == False:
            lista = webScrapping(nombre)
            rating = float(lista[0])
            precio_final = lista[1]
            url = lista[2]
            if rating < 4.5:
                recomendado = False
            else:
                recomendado = True
            categoria_final = categoriaDelProducto(nombre)
            p = Producto(nombre=nombre, price=precio_final,
                         rating=rating, recomendado=recomendado,
                         categoria=categoria_final, url=url, imagen=imagen)
            p.save()
            if (recomendado == False):
                lista = recomendarProducto(categoria_final, precio_final)
                nombre2 = lista[0]
                precio2 = lista[1]
                rating2 = lista[2]
                url2 = lista[3]
                imagen2 = lista[4]
                dicc = {"productos": top5, "nombre2": nombre2,
                        "valoracion2": rating2, "precio2": precio2, "portal2": url2,
                        "imagen2": imagen2, "categorias": categorias, "nombre": nombre,
                        "valoracion": rating, "precio": precio_final, "portal": url,
                        "imagen": imagen}
                return render(request, 'inicio.html', dicc)
            else:
                dicc = {"productos": top5, "nombre": nombre,
                        "valoracion": rating, "precio": precio_final, "portal": url,
                        "imagen": imagen, "categorias": categorias}
                return render(request, 'inicio.html', dicc)
        else:
            lista = informacionDElProducto(nombre)
            rating = lista[0]
            precio_final = lista[1]
            url = lista[2]
            if rating < 4.5:
                recomendado = False
            else:
                recomendado = True
            if (recomendado == False):
                lista = recomendarProducto(categoria_final, precio_final)
                nombre2 = lista[0]
                precio2 = lista[1]
                rating2 = lista[2]
                url2 = lista[3]
                imagen2 = lista[4]
                dicc = {"productos": top5, "nombre2": nombre2,
                        "valoracion2": rating2, "precio2": precio2, "portal2": url2,
                        "imagen2": imagen2, "categorias": categorias, "nombre": nombre,
                        "valoracion": rating, "precio": precio_final, "portal": url,
                        "imagen": imagen}
                return render(request, 'inicio.html', dicc)
            else:
                dicc = {"productos": top5, "nombre": nombre,
                        "valoracion": rating, "precio": precio_final, "portal": url,
                        "imagen": imagen, "categorias": categorias}
                return render(request, 'inicio.html', dicc)


def confirmacion(request):
    return render(request, 'confirmacion.html')
