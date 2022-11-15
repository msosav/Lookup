import time
import schedule
from pymongo import MongoClient
from Scrapping.scraping import web_scrapping

cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["productos"]
col = db["Aplicacion_producto"]

def nombre_documentos():
    documentos = list()
    nombreDocumentos = list()
    cont = 0
    for documento in col.find({}, {"nombre": 1}):
        documentos.append(documento)
        nombreDocumentos.append(documentos[cont]["nombre"])
        cont += 1
    
    for nombre in nombreDocumentos:
        lista = web_scrapping(nombre)
        nombreProductoBuscado = lista[0]
        imagenProductoBuscado = lista[1]
        urlProductoBuscado = lista[2]
        precioProductoBuscado = lista[3]
        ratingProductoBuscado = lista[4]
        ratingDeLosComentariosProductoBuscado = lista[5]
        primerComentarioProductoBuscado = lista[6][0]
        segundoComentarioProductoBuscado = lista[6][1]

        col.update_one({"nombre":nombre}, {
            "$set": {"precio": precioProductoBuscado, "rating":ratingProductoBuscado, 
            "url": urlProductoBuscado, "imagen": imagenProductoBuscado, "primer_comentario":primerComentarioProductoBuscado,
            "segundo_comentario":segundoComentarioProductoBuscado, "rating_modelo":ratingDeLosComentariosProductoBuscado
            }
        })    

def actualizacion_cada_24_horas():
    schedule.every(24).hours.do(nombre_documentos)

    while True:
        schedule.run_pending()
        time.sleep(1)

