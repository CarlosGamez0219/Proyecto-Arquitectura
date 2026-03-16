from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import EstadisticaGeneral, Partida
import json

# ─── AUTH ────────────────────────────────────────────────────────────────────

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('seleccionar_nivel')
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'memory_game/login.html', {'error': error})


def registro_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            error = 'Ese nombre de usuario ya está en uso.'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('seleccionar_nivel')
    return render(request, 'memory_game/registro.html', {'error': error})


# ─── JUEGO ───────────────────────────────────────────────────────────────────

@login_required
def seleccionar_nivel(request):
    return render(request, 'memory_game/nivel.html')


@login_required
def jugar(request):
    nivel = request.GET.get('nivel', 'Básico')

    config = {
        'Básico':   {'intentos': 6, 'tiempo': 60},
        'Medio':    {'intentos': 4, 'tiempo': 45},
        'Avanzado': {'intentos': 2, 'tiempo': 30},
    }
    cfg = config.get(nivel, config['Básico'])

    return render(request, 'memory_game/tablero.html', {
        'nivel':    nivel,
        'intentos': cfg['intentos'],
        'tiempo':   cfg['tiempo'],
    })


@login_required
def registrar_partida(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        Partida.objects.create(
            usuario=user,
            nivel=data['nivel'],
            resultado=data['resultado'],
            tiempo_segundos=data['tiempo'],
            intentos_realizados=data['intentos']
        )

        stats, _ = EstadisticaGeneral.objects.get_or_create(usuario=user)

        if data['resultado'] == 'Victoria':
            stats.victorias += 1
        else:
            stats.derrotas += 1

        if data['nivel'] == 'Básico':
            stats.jugadas_basico += 1
        elif data['nivel'] == 'Medio':
            stats.jugadas_medio += 1
        elif data['nivel'] == 'Avanzado':
            stats.jugadas_avanzado += 1

        total_nuevo = stats.total_partidas + 1
        stats.tiempo_promedio = (
            (stats.tiempo_promedio * stats.total_partidas) + data['tiempo']
        ) / total_nuevo
        stats.total_partidas = total_nuevo
        stats.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=405)


# ─── PERFIL ──────────────────────────────────────────────────────────────────

@login_required
def ver_perfil(request):
    stats, _ = EstadisticaGeneral.objects.get_or_create(usuario=request.user)
    historial = Partida.objects.filter(
        usuario=request.user
    ).order_by('-fecha')[:10]

    return render(request, 'memory_game/perfil.html', {
        'stats':    stats,
        'historial': historial,
    })