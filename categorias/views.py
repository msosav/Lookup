from django.shortcuts import render
from funciones import analiticas, productosPorCategoria
# Create your views here.


def categoriaBuscada(request):
    top5 = analiticas()
    categorias = ["Electronicos", "Electrodomesticos", "Hogar"]
    if request.method == 'POST':
        categoria = request.POST.get("categorias")
    productos = productosPorCategoria(categoria)
    dicc = {"productos_de_la_categoria": productos,
            "categoria": categoria, "categorias": categorias,
            "productos": top5}
    return render(request, 'pagina_de_categorias.html', dicc)
