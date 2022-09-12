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
