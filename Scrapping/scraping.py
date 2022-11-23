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

    portalesWeb = comprobarProducto(producto.lower(), portalesWeb)

    infoProducto = precioMenor(portalesWeb)
    print(infoProducto)
    nombreDelProducto = infoProducto[0]
    imagenDelProducto = infoProducto[1]
    urlDelProducto = infoProducto[2]
    precioDelProducto = infoProducto[3]

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

    return (nombreDelProducto, imagenDelProducto, urlDelProducto, precioDelProducto,
            ratingDelProducto, ratingDeLosComentarios, comentariosRelevantes)


def precioMenor(portalesWeb):
    if len(portalesWeb) == 1:
        urlDelProducto = portalesWeb[0][2]
        imagenDelProducto = portalesWeb[0][1]
        nombreDelProducto = portalesWeb[0][0]
        precioDelProducto = portalesWeb[0][3]
        return (nombreDelProducto, imagenDelProducto, urlDelProducto, precioDelProducto)
    for portal in range(len(portalesWeb)):
        if portal == 0:
            urlDelProducto = portalesWeb[0][2]
            imagenDelProducto = portalesWeb[0][1]
            nombreDelProducto = portalesWeb[0][0]
            precioDelProducto = portalesWeb[0][3]
        elif portalesWeb[portal][3] < portalesWeb[portal-1][3]:
            urlDelProducto = portalesWeb[portal][2]
            imagenDelProducto = portalesWeb[portal][1]
            nombreDelProducto = portalesWeb[portal][0]
            precioDelProducto = portalesWeb[portal][3]
    return (nombreDelProducto, imagenDelProducto, urlDelProducto, precioDelProducto)


def comprobarProducto(producto, portalesWeb):
    lista = []
    for portal in portalesWeb:
        if (portal[0].lower().__contains__(producto)):
            if (producto.lower().__contains__("accesorio") or
                producto.lower().__contains__("carcasa") or
                    producto.lower().__contains__("cargador")):
                lista.append(portal)
            elif (portal[0].lower().__contains__("accesorio") or
                  portal[0].lower().__contains__("carcasa") or
                  portal[0].lower().__contains__("cargador")):
                pass
            else:
                lista.append(portal)
    return lista
