from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Juego
    path('nivel/', views.seleccionar_nivel, name='seleccionar_nivel'),
    path('jugar/', views.jugar, name='jugar_memoria'),
    path('registrar-partida/', views.registrar_partida, name='registrar_partida'),

    # Perfil
    path('perfil/', views.ver_perfil, name='perfil'),
]