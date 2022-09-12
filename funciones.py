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
    #analiticas.sort()
    for elemento in range(0, len(analiticas)):
        analiticas[elemento] = analiticas[elemento].capitalize()
    top_5 = analiticas[0:5]
    return top_5

def productosPorCategoria():
    lista_electronicos = []
    lista_electrodomesticos = []
    lista_hogar = []
    for documentos in collection.find():
        if documentos["categoria"] == "Electronicos":
            if documentos["categoria"] not in lista_electronicos:
                lista_electronicos.append(documentos["nombre"])
        elif documentos["categoria"] == "Electrodomesticos":
            if documentos["categoria"] not in lista_electrodomesticos:
                lista_electrodomesticos.append(documentos["nombre"])
        elif documentos["categoria"] == "Hogar":
            if documentos["categoria"] not in lista_hogar:
                lista_hogar.append(documentos["nombre"])
    return lista_electronicos, lista_electrodomesticos, lista_hogar
