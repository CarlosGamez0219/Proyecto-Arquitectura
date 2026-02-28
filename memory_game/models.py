from django.db import models

from django.contrib.auth.models import User

# MODELO 1: Resumen General.
class EstadisticaGeneral(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    jugadas_basico = models.IntegerField(default=0)
    jugadas_medio = models.IntegerField(default=0)
    jugadas_avanzado = models.IntegerField(default=0)
    tiempo_promedio = models.FloatField(default=0.0)
    total_partidas = models.IntegerField(default=0)

    @property
    def nivel_mas_jugado(self):
        niveles = {
            'Básico': self.jugadas_basico,
            'Medio': self.jugadas_medio,
            'Avanzado': self.jugadas_avanzado
        }
        if self.total_partidas == 0: return "N/A"
        return max(niveles, key=niveles.get)

    def __str__(self):
        return f"Resumen de {self.usuario.username}"

# MODELO 2: Historial Detallado.
class Partida(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historial')
    fecha = models.DateTimeField(auto_now_add=True)
    nivel = models.CharField(max_length=20)
    resultado = models.CharField(max_length=10) # 'Victoria' o 'Derrota'
    tiempo_segundos = models.IntegerField()
    intentos_realizados = models.IntegerField()

    def __str__(self):
        return f"Partida {self.id} - {self.usuario.username}"
