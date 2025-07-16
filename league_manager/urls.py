from django.urls import path
from .views import (
    TeamListView, 
    TeamCreateView, 
    TeamUpdateView, 
    TeamDeleteView,
    upload_result_file,
    LeagueStandingsView
)

urlpatterns = [
    path('', LeagueStandingsView.as_view(), name='home'),
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/new/', TeamCreateView.as_view(), name='team_create'),
    path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    
    # Rota para upload de resultados
    path('results/upload/', upload_result_file, name='upload_result'),

    # Rota para a classificação da liga
    path('standings/', LeagueStandingsView.as_view(), name='league_standings'),
] 