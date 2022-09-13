from pymongo import MongoClient
cluster = MongoClient(
    "mongodb+srv://sergiocordobam:12345@cluster0.qbfcw.mongodb.net/test")
db = cluster["lookup"]
collection = db["Aplicacion_producto"]


def analiticas():
    analiticas = []
    for documentos in collection.find():
        if collection.count_documents({"nombre": documentos["nombre"]}) >= 1:
            if documentos["nombre"] not in analiticas:
                analiticas.append(documentos["nombre"])
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


def categoriaDelProducto(nombre):
    electronicos = ["iphone", "samsung", "moto", "hp", "asus"]
    electrodomesticos = ["televisor", "plancha", "nevera", "ventilador"]
    hogar = ["silla", "mesa", "cama"]
    categorias = [electronicos, electrodomesticos, hogar]

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


def recomendarProducto(categoria, precio):
    for productos in collection.find():
        if productos["categoria"] == categoria:
            if (productos["price"] <= precio + 700):
                if (productos["recomendado"] == True):
                    return (productos["nombre"], productos["price"],
                            productos["rating"], productos["url"],
                            productos["imagen"])
    return "No hay productos que recomendar"
