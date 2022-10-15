"""Lookup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from categorias.views import categoriaBuscada
from Aplicacion.views import confirmacion, historial, inicio, productoBuscado, prueba, prueba2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name="inicio"),
    path('historial/', historial, name="historial"),
    path('confirmacion/', confirmacion),
    path('categoria/', categoriaBuscada, name="categoria"),
    path('producto/', productoBuscado, name="producto"),
    path('prueba/', prueba, name="prueba"),
    path('prueba2/', prueba2, name="prueba2"),
]
