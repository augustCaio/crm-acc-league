import json
from datetime import timedelta
from .models import Driver, Team, Event, RaceResult

def parse_acc_results_json(json_content, event):
    """
    Processa o conteúdo de um arquivo JSON de resultado do ACC e
    salva os dados no banco de dados, associando-os a um evento.
    """
    try:
        data = json.loads(json_content)
    except json.JSONDecodeError:
        # Lidar com erro de JSON inválido
        return {"error": "Arquivo JSON inválido."}

    race_results = data.get("sessionResult", {}).get("leaderBoardLines", [])
    
    for result in race_results:
        driver_info = result.get("currentDriver", {})
        player_name = f"{driver_info.get('firstName', '')} {driver_info.get('lastName', '')}".strip()
        
        if not player_name:
            continue

        # Procura ou cria o piloto
        driver, _ = Driver.objects.get_or_create(full_name=player_name)

        # Procura ou cria a equipe (se houver)
        team_name = result.get("car", {}).get("teamName", "")
        team = None
        if team_name:
            team, _ = Team.objects.get_or_create(name=team_name)
            # Associa o piloto à equipe se ele não tiver uma
            if not driver.team:
                driver.team = team
                driver.save()
        
        # Converte o melhor tempo de volta de milissegundos para timedelta
        best_lap_ms = result.get("timing", {}).get("bestLap", 0)
        best_lap_time = timedelta(milliseconds=best_lap_ms) if best_lap_ms > 0 else None

        # Cria ou atualiza o RaceResult
        RaceResult.objects.update_or_create(
            event=event,
            driver=driver,
            defaults={
                'team': team,
                'car_model': result.get("car", {}).get("carModel", ""),
                'final_position': result.get("car", {}).get("raceNumber", 0), # Usando raceNumber como fallback para posição
                'best_lap_time': best_lap_time,
                'incidents': 0,  # O JSON padrão não parece ter contagem de incidentes
                'points_earned': 0, # A pontuação será calculada depois
                'raw_json_data': result # Salva o objeto de resultado do piloto
            }
        )
        
    return {"success": f"{len(race_results)} resultados processados."} 