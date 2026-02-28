from django.urls import path
from . import views

urlpatterns = [
    # Esta será la ruta para guardar los datos al terminar el juego
    path('jugar/', views.jugar, name='jugar_memoria'),
    path('registrar-partida/', views.registrar_partida, name='registrar_partida'),
    path('perfil/', views.ver_perfil, name='perfil'),
]