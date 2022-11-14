from Scrapping.super_exito import busqueda_exito
from Scrapping.ktronix import busqueda_ktronix
from Scrapping.mercadoLibre import busqueda_mercadolibre

from lenguaje_natural import procesamiento


def web_scrapping(producto):
    mercadoLibre = busqueda_mercadolibre(producto)
    ktronix = busqueda_ktronix(producto)
    exito = busqueda_exito(producto)

    portalesWeb = [mercadoLibre, ktronix, exito]

    if len(exito) == 4:
        ratingDelProducto = (portalesWeb[0][4] + portalesWeb[1][4])/2
        comentarios = portalesWeb[0][5] + portalesWeb[1][5]
    else:
        ratingDelProducto = (
            portalesWeb[0][4] + portalesWeb[1][4] + portalesWeb[2][4])/3
        comentarios = portalesWeb[0][5] + portalesWeb[1][5] + portalesWeb[2][5]
    precioDelProducto = min(
        portalesWeb[0][3], portalesWeb[1][3], portalesWeb[2][3])
    cantidadDeComentarios = len(comentarios)
    comentariosBuenos = 0
    comentariosMalos = 0

    comentariosRelevantesAux = ["", "", "", ""]

    for comentario in comentarios:
        buenoOMalo = procesamiento(comentario)
        if (buenoOMalo):
            if comentariosBuenos <= 1:
                comentariosRelevantesAux[comentariosBuenos] = comentario
            comentariosBuenos = comentariosBuenos + 1
        else:
            if comentariosMalos <= 1:
                comentariosRelevantesAux[comentariosMalos+2] = comentario
            comentariosMalos = comentariosMalos + 1

    ratingDeLosComentarios = (5/cantidadDeComentarios)*comentariosBuenos

    if ratingDelProducto > 4.5:
        comentariosRelevantes = [
            comentariosRelevantesAux[0], comentariosRelevantesAux[1]]
    elif ratingDelProducto > 3.8:
        comentariosRelevantes = [
            comentariosRelevantesAux[0], comentariosRelevantesAux[2]]
    else:
        comentariosRelevantes = [
            comentariosRelevantesAux[2],  comentariosRelevantesAux[3]]

    if (portalesWeb[0][3] == precioDelProducto):
        urlDelProducto = portalesWeb[0][2]
        imagenDelProducto = portalesWeb[0][1]
        nombreDelProducto = portalesWeb[0][0]
    elif (portalesWeb[1][3] == precioDelProducto):
        urlDelProducto = portalesWeb[1][2]
        imagenDelProducto = portalesWeb[1][1]
        nombreDelProducto = portalesWeb[1][0]
    else:
        urlDelProducto = portalesWeb[2][2]
        imagenDelProducto = portalesWeb[2][1]
        nombreDelProducto = portalesWeb[2][0]

    return (nombreDelProducto, imagenDelProducto, urlDelProducto, precioDelProducto,
            ratingDelProducto, ratingDeLosComentarios, comentariosRelevantes)
