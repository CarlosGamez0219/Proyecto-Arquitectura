from django.shortcuts import render
from django.http import JsonResponse
from .models import EstadisticaGeneral, Partida
import json

def registrar_partida(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        
        # 1. Crear el registro en el Historial (Modelo Partida)
        nueva_partida = Partida.objects.create(
            usuario=user,
            nivel=data['nivel'],
            resultado=data['resultado'],
            tiempo_segundos=data['tiempo'],
            intentos_realizados=data['intentos']
        )
        
        # 2. Actualizar el Resumen General (Modelo EstadisticaGeneral)
        stats, created = EstadisticaGeneral.objects.get_or_create(usuario=user)
        
        if data['resultado'] == 'Victoria':
            stats.victorias += 1
        else:
            stats.derrotas += 1
            
        # Actualizar contador de nivel
        if data['nivel'] == 'Básico': stats.jugadas_basico += 1
        elif data['nivel'] == 'Medio': stats.jugadas_medio += 1
        elif data['nivel'] == 'Avanzado': stats.jugadas_avanzado += 1
        
        # Recalcular tiempo promedio
        stats.tiempo_promedio = ((stats.tiempo_promedio * stats.total_partidas) + data['tiempo']) / (stats.total_partidas + 1)
        stats.total_partidas += 1
        stats.save()

        
        
        return JsonResponse({'status': 'success'})
        
def jugar(request):
    # Por ahora solo renderizamos el template
    return render(request, 'memory_game/tablero.html')

#login_required
def ver_perfil(request):
    # Esto busca las estadísticas del usuario o las crea si no existen
    stats, created = EstadisticaGeneral.objects.get_or_create(usuario=request.user)
    
    # Esto trae las últimas 10 partidas
    historial = Partida.objects.filter(usuario=request.user).order_by('-fecha')[:10]
    
    return render(request, 'memory_game/perfil.html', {
        'stats': stats,
        'historial': historial
    })
