from django.db import models

# Create your models here.

class Team(models.Model):
    """Representa uma equipe de corrida."""
    name = models.CharField(max_length=100, unique=True, help_text="Nome da equipe")
    
    def __str__(self):
        return self.name

class Driver(models.Model):
    """Representa um piloto."""
    full_name = models.CharField(max_length=150, unique=True, help_text="Nome completo do piloto")
    nickname = models.CharField(max_length=50, blank=True, null=True, help_text="Apelido do piloto")
    nationality = models.CharField(max_length=50, blank=True, null=True, help_text="Nacionalidade do piloto")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='drivers', null=True, blank=True, help_text="Equipe à qual o piloto pertence")

    def __str__(self):
        return self.full_name

class Event(models.Model):
    """Representa um evento de corrida, como uma etapa do campeonato."""
    name = models.CharField(max_length=200, help_text="Nome do evento (ex: Etapa 1 - Monza)")
    track_name = models.CharField(max_length=100, help_text="Nome da pista")
    event_date = models.DateField(help_text="Data do evento")

    def __str__(self):
        return self.name

class RaceResult(models.Model):
    """Armazena o resultado de um único piloto em um evento."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='results', help_text="Evento ao qual este resultado pertence")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='results', help_text="Piloto associado a este resultado")
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, help_text="Equipe do piloto na corrida")
    car_model = models.CharField(max_length=100, help_text="Modelo do carro utilizado")
    final_position = models.PositiveIntegerField(help_text="Posição final na corrida")
    best_lap_time = models.DurationField(null=True, blank=True, help_text="Melhor tempo de volta")
    incidents = models.PositiveIntegerField(default=0, help_text="Número de incidentes")
    points_earned = models.PositiveIntegerField(default=0, help_text="Pontos conquistados na corrida")
    raw_json_data = models.JSONField(default=dict, help_text="Dados brutos do arquivo JSON de resultado")

    class Meta:
        # Garante que um piloto só pode ter um resultado por evento
        unique_together = ('event', 'driver')
        ordering = ['final_position']

    def __str__(self):
        return f"{self.event} - {self.driver} - P{self.final_position}"
