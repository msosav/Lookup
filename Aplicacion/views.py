from django.shortcuts import render
from Scrapping.scraping import web_scrapping
from Aplicacion.models import Producto
from pymongo import MongoClient
from funciones import analiticas, buscar_producto_en_BD, informacion_del_producto, categoria_del_producto, recomendar_producto
from actualizacion_periodica import actualizacion_cada_24_horas

# Se conecta a la base de datos
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["productos"]
collection = db["Aplicacion_producto"]

# Create your views here.

# Variables globales
top5 = analiticas()
categorias = ["Electronicos", "Electrodomesticos", "Hogar"]
actualizacion_cada_24_horas()


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
        nombreProductoBuscadoAux = buscar_producto_en_BD(nombreProductoBuscado)
        if nombreProductoBuscadoAux == False:
            context = crear_producto(nombreProductoBuscado)
        else:
            context = buscar_producto(nombreProductoBuscadoAux)
        return render(request, 'inicio.html', context)
    return render(request, 'inicio.html', context)


def crear_producto(nombreProductoBuscadoAux):
    lista = web_scrapping(nombreProductoBuscadoAux)
    nombreProductoBuscado = lista[0]
    imagenProductoBuscado = lista[1]
    urlProductoBuscado = lista[2]
    precioProductoBuscado = lista[3]
    ratingProductoBuscado = lista[4]
    ratingDeLosComentariosProductoBuscado = lista[5]
    primerComentarioProductoBuscado = lista[6][0]
    segundoComentarioProductoBuscado = lista[6][1]
    if ratingProductoBuscado < 4.5:
        recomendado = False
    else:
        recomendado = True
    categoriaFinal = categoria_del_producto(nombreProductoBuscado)
    producto = Producto(nombre=nombreProductoBuscado, precio=precioProductoBuscado,
                        rating=ratingProductoBuscado, recomendado=recomendado,
                        categoria=categoriaFinal, url=urlProductoBuscado, imagen=imagenProductoBuscado,
                        primer_comentario=primerComentarioProductoBuscado, segundo_comentario=segundoComentarioProductoBuscado,
                        rating_modelo=ratingDeLosComentariosProductoBuscado)
    producto.save()
    if (recomendado == False):
        context = producto_recomendado(categoriaFinal, precioProductoBuscado, nombreProductoBuscado,
                                       ratingProductoBuscado, urlProductoBuscado)
    else:
        context = {"productos": top5, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagenProductoBuscado, "categorias": categorias,
                   "primer_comentario": primerComentarioProductoBuscado, "segundo_comentario": segundoComentarioProductoBuscado,
                   "rating_modelo": ratingDeLosComentariosProductoBuscado}

    return context


def producto_recomendado(informacionProductoBuscado):
    # informacion del producto buscado
    ratingProductoBuscado = informacionProductoBuscado[0]
    precioProductoBuscado = informacionProductoBuscado[1]
    urlProductoBuscado = informacionProductoBuscado[2]
    imagenProductoBuscado = informacionProductoBuscado[3]
    primerComentarioProductoBuscado = informacionProductoBuscado[4]
    segundoComentarioProductoBuscado = informacionProductoBuscado[5]
    ratingModeloProductoBuscado = informacionProductoBuscado[6]
    categoriaFinal = informacionProductoBuscado[7]
    nombreProductoBuscado = informacionProductoBuscado[8]

    # informacion del producto recomendado
    informacionProductoRecomendado = recomendar_producto(
        categoriaFinal, precioProductoBuscado, nombreProductoBuscado)
    if informacionProductoRecomendado != False:
        nombreProductoRecomendado = informacionProductoRecomendado[0]
        precioProductoRecomendado = informacionProductoRecomendado[1]
        ratingProductoRecomendado = informacionProductoRecomendado[2]
        urlProductoRecomendado = informacionProductoRecomendado[3]
        imagenProductoRecomendado = informacionProductoRecomendado[4]
        primerComentarioProductoRecomendado = informacionProductoRecomendado[5]
        segundoComentarioProductoRecomedado = informacionProductoRecomendado[6]
        context = {"productos": top5, "nombre2": nombreProductoRecomendado,
                   "valoracion2": ratingProductoRecomendado, "precio2": precioProductoRecomendado,
                   "portal2": urlProductoRecomendado, "imagen2": imagenProductoRecomendado,
                   "categorias": categorias, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagenProductoBuscado, "primer_comentario": primerComentarioProductoBuscado,
                   "segundo_comentario": segundoComentarioProductoBuscado,
                   "primer_comentario2": primerComentarioProductoRecomendado,
                   "segundo_comentario2": segundoComentarioProductoRecomedado}
        return context
    else:
        context = {"productos": top5, "categorias": categorias, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagenProductoBuscado, "primer_comentario": primerComentarioProductoBuscado,
                   "segundo_comentario": segundoComentarioProductoBuscado, "recomendacion": True}
        return context


def buscar_producto(nombreProductoBuscado):
    informacionProductoBuscado = informacion_del_producto(
        nombreProductoBuscado)
    ratingProductoBuscado = informacionProductoBuscado[0]
    precioProductoBuscado = informacionProductoBuscado[1]
    urlProductoBuscado = informacionProductoBuscado[2]
    imagenProductoBuscado = informacionProductoBuscado[3]
    primerComentarioProductoBuscado = informacionProductoBuscado[4]
    segundoComentarioProductoBuscado = informacionProductoBuscado[5]
    ratingModeloProductoBuscado = informacionProductoBuscado[6]
    if ratingProductoBuscado < 4.5:
        recomendado = False
    else:
        recomendado = True
    if (recomendado == False):
        context = producto_recomendado(informacionProductoBuscado)
    else:
        context = {"productos": top5, "nombre": nombreProductoBuscado,
                   "valoracion": ratingProductoBuscado, "precio": precioProductoBuscado, "portal": urlProductoBuscado,
                   "imagen": imagenProductoBuscado, "categorias": categorias,
                   "primer_comentario": primerComentarioProductoBuscado, "segundo_comentario": segundoComentarioProductoBuscado,
                   "rating_modelo": ratingModeloProductoBuscado}
    return context


def confirmacion(request):
    return render(request, 'confirmacion.html')
