from django.shortcuts import render
from scraping import webScrapping
from Aplicacion.models import Producto
from pymongo import MongoClient
from funciones import analiticas, buscarProducto, informacionDElProducto, categoriaDelProducto, recomendarProducto

# Se conecta a la base de datos
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["lookup"]
collection = db["productos"]

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
            primer_comentario = lista[4][0]
            segundo_comentario = lista[4][1]
            if rating < 4.5:
                recomendado = False
            else:
                recomendado = True
            categoria_final = categoriaDelProducto(nombre)
            p = Producto(nombre=nombre, precio=precio_final,
                         rating=rating, recomendado=recomendado,
                         categoria=categoria_final, url=url, imagen=imagen,
                         primer_comentario=primer_comentario, segundo_comentario=segundo_comentario)
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


def prueba(request):
    global top5, categorias, imagen
    nombre = "IPhone 13"
    precio_final = 3000000
    rating = 3.5
    url = "google.com"
    nombre2 = "IPhone 12"
    precio2 = 2500000
    rating2 = 4.5
    url2 = "yahoo.com"
    imagen2 = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fonecomm.bm%2Fwp-content%2Fuploads%2F2021%2F01%2FScreen-Shot-2021-01-29-at-11.23.16-AM.jpg&f=1&nofb=1&ipt=146bbfae91ebd63bb4336e2e1f6418de317565fd292fb5a1afe0a1e5d2c5ddb6&ipo=images"
    dicc = {"productos": top5, "nombre2": nombre2,
            "valoracion2": rating2, "precio2": precio2, "portal2": url2,
            "imagen2": imagen2, "categorias": categorias, "nombre": nombre,
            "valoracion": rating, "precio": precio_final, "portal": url,
            "imagen": imagen}
    return render(request, 'inicio.html', dicc)


def prueba2(request):
    global top5, categorias, imagen
    nombre = "IPhone 13"
    precio_final = 3000000
    rating = 3.5
    url = "google.com"
    primer_comentario = "Muy bueno, me encantó"
    segundo_comentario = "Muy bueno, muy fácil de usar"
    dicc = {"productos": top5, "categorias": categorias, "nombre": nombre,
            "valoracion": rating, "precio": precio_final, "portal": url,
            "imagen": imagen, "primer_comentario": primer_comentario,
            "segundo_comentario": segundo_comentario}
    return render(request, 'inicio.html', dicc)
