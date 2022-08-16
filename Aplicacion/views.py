from django.http import HttpResponseRedirect
from django.shortcuts import render
from scraping import getMercadoLibre

# Create your views here.
def inicio(request):
    productos = ["Mac", "IPhone 13", "Jordan Retro XI"]
    nombre = "IPhone 13"
    #precio = 1250
    portal = "https://www.amazon.es/Apple-iPhone-13-128-GB-Azul/dp/B09G9DMQ7M"
    imagen = "https://m.media-amazon.com/images/I/613AVx005lL._AC_SX522_.jpg"
    caracteristicas = ["Pantalla Super Retina XDR de 6,1 pulgadas",
                        "El modo Cine añade poca profundidad de campo y cambia el enfoque automáticamente en los vídeos", "Sistema avanzado de cámara dual de 12 Mpx con gran angular y ultra gran angular, Estilos Fotográficos, HDR Inteligente 4, modo Noche y grabación de vídeo en 4K HDR con Dolby Vision"]
    if request.method == 'POST':
        lista = getMercadoLibre("iphone 13")
        rating = lista[0]
        precio = lista[1]
        #rating = lista[0]
        return render(request, 'inicio.html', {"productos":productos, "nombre":nombre,
                            "valoracion":rating, "precio":precio, "portal":portal,
                            "imagen":imagen, "caracteristicas":caracteristicas})
    return render(request, 'inicio.html')

def historial(request):
    return render(request, 'historial.html')

def confirmacion(request):
    return render(request, 'confirmacion.html')