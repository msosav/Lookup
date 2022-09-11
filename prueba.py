nombre = request.POST.get("producto_buscado").capitalize()
lista = getMercadoLibre(nombre)
 rating = lista[0]
  precio = lista[1]
   url = lista[2]
    electronicos = ["iphone", "samsung", "moto", "hp", "asus"]
     electrodomesticos = ["televisor", "plancha", "nevera", "ventilador"]
      hogar = ["silla", "mesa", "cama"]
       if float(rating) < 4.6:
            recomendado = False
        else:
            recomendado = True

        for elemento in range(len(electronicos)):
            if nombre.lower().__contains__(electronicos[elemento]):
                categoria_final = "Electronicos"
                p = Producto(nombre=nombre, price=precio,
                             rating=rating, recomendado=recomendado, categoria=categoria_final)
                p.save()

        for elemento in range(len(electrodomesticos)):
            if nombre.lower().__contains__(electrodomesticos[elemento]):
                categoria_final = "Electrodomesticos"
                p = Producto(nombre=nombre, price=precio,
                             rating=rating, recomendado=recomendado, categoria=categoria_final)
                p.save()

        for elemento in range(len(hogar)):
            if nombre.lower().__contains__(hogar[elemento]):
                categoria_final = "Hogar"
                p = Producto(nombre=nombre, price=precio,
                             rating=rating, recomendado=recomendado, categoria=categoria_final)
                p.save()

        if (recomendado == False):
            return render(request, 'inicio.html', {"productos": top5, "nombre2": "funciona",
                                                   "valoracion2": rating, "precio2": precio, "portal2": url,
                                                   "imagen2": imagen, "caracteristicas2": caracteristicas, })
        else:
            return render(request, 'inicio.html', {"productos": top5, "nombre": nombre,
                                                   "valoracion": rating, "precio": precio, "portal": url,
                                                   "imagen": imagen, "caracteristicas": caracteristicas, })