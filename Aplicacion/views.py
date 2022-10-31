from django.shortcuts import render
from scraping import webScrapping
from Aplicacion.models import Producto
from pymongo import MongoClient
from funciones import analiticas, buscar_producto, informacion_del_producto, categoria_del_producto, recomendar_producto

# Se conecta a la base de datos
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["productos"]
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


def producto_buscado(request):
    global top5, categorias, imagen, caracteristicas
    if request.method == 'POST':
        nombreProductoBuscado = request.POST.get(
            "producto_buscado").capitalize()
        if buscar_producto(nombreProductoBuscado) == False:
            context = crear_producto(nombreProductoBuscado)
        else:
            context = buscar_producto(nombreProductoBuscado)
        return render(request, 'inicio.html', context)
    return render(request, 'inicio.html', context)


def crear_producto(nombreProductoBuscado):
    lista = webScrapping(nombreProductoBuscado)
    ratingProductoBuscado = float(lista[0])
    precioProductoBuscado = lista[1]
    urlProductoBuscado = lista[2]
    ratingModeloProductoBuscado = lista[3]
    primerComentarioProductoBuscado = lista[4][0]
    segundoComentarioProductoBuscado = lista[4][1]
    if ratingProductoBuscado < 4.5:
        recomendado = False
    else:
        recomendado = True
    categoriaFinal = categoria_del_producto(nombreProductoBuscado)
    producto = Producto(nombre=nombreProductoBuscado, precio=precioProductoBuscado,
                        rating=ratingProductoBuscado, recomendado=recomendado,
                        categoria=categoriaFinal, url=urlProductoBuscado, imagen=imagen,
                        primer_comentario=primerComentarioProductoBuscado, segundo_comentario=segundoComentarioProductoBuscado,
                        rating_modelo=ratingModeloProductoBuscado)
    producto.save()
    if (recomendado == False):
        context = producto_recomendado(categoriaFinal, precioProductoBuscado, nombreProductoBuscado,
                                       ratingProductoBuscado, urlProductoBuscado)
    else:
        context = {"productos": top5, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagen, "categorias": categorias,
                   "primer_comentario": primerComentarioProductoBuscado, "segundo_comentario": segundoComentarioProductoBuscado,
                   "rating_modelo": ratingModeloProductoBuscado}

    return context


def producto_recomendado(categoriaFinal, precioProductoBuscado, nombreProductoBuscado,
                         ratingProductoBuscado, urlProductoBuscado):
    lista = recomendar_producto(
        categoriaFinal, precioProductoBuscado)
    nombreProductoRecomendado = lista[0]
    precioProductoRecomendado = lista[1]
    ratingProductoRecomendado = lista[2]
    urlProductoRecomendado = lista[3]
    imagenProductoRecomendado = lista[4]
    context = {"productos": top5, "nombre2": nombreProductoRecomendado,
               "valoracion2": ratingProductoRecomendado, "precio2": precioProductoRecomendado,
               "portal2": urlProductoRecomendado, "imagen2": imagenProductoRecomendado,
               "categorias": categorias, "nombre": nombreProductoBuscado,
               "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
               "imagen": imagen}
    return context


def buscar_producto(nombreProductoBuscado):
    lista = informacion_del_producto(nombreProductoBuscado)
    ratingProductoBuscado = lista[0]
    precioProductoBuscado = lista[1]
    urlProductoBuscado = lista[2]
    imagen = lista[3]
    primerComentarioProductoBuscado = lista[4]
    segundoComentarioProductoBuscado = lista[5]
    ratingModeloProductoBuscado = lista[6]
    categoriaFinal = lista[7]
    if ratingProductoBuscado < 4.5:
        recomendado = False
    else:
        recomendado = True
    if (recomendado == False):
        context = producto_recomendado(categoriaFinal, precioProductoBuscado,
                                       nombreProductoBuscado, ratingProductoBuscado, urlProductoBuscado)
    else:
        context = {"productos": top5, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagen, "categorias": categorias,
                   "primer_comentario": primerComentarioProductoBuscado, "segundo_comentario": segundoComentarioProductoBuscado,
                   "rating_modelo": ratingModeloProductoBuscado}
    return context


def confirmacion(request):
    return render(request, 'confirmacion.html')
