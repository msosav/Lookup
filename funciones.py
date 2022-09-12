from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["lookup"]
collection = db["Aplicacion_producto"]


def analiticas():
    analiticas = []
    for documentos in collection.find():
        if collection.count_documents({"nombre": documentos["nombre"]}) >= 1:
            if documentos["nombre"].lower() not in analiticas:
                analiticas.append(documentos["nombre"])
    # analiticas.sort()
    for elemento in range(0, len(analiticas)):
        analiticas[elemento] = analiticas[elemento].capitalize()
    top_5 = analiticas[0:5]
    return top_5


def productosPorCategoria(categoria):
    lista = []
    for documentos in collection.find():
        if documentos["categoria"] == categoria:
            if documentos["nombre"] not in lista:
                lista.append(documentos["nombre"])
    return lista


def categoriaDelProducto(nombre, categorias):
    contador = 0
    for categoria in categorias:
        for elemento in categoria:
            if nombre.lower().__contains__(elemento):
                if contador == 0:
                    categoria_final = "Electronicos"
                    break
                if contador == 1:
                    categoria_final = "Electrodomesticos"
                    break
                if contador == 2:
                    categoria_final = "Hogar"
                    break
        contador += 1
    return categoria_final
