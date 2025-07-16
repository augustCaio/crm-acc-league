import json
from django.test import TestCase
from datetime import date
from .models import Driver, Team, Event, RaceResult
from .utils import parse_acc_results_json
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UtilsTestCase(TestCase):
    def setUp(self):
        """Prepara dados iniciais para os testes."""
        self.event = Event.objects.create(
            name="Test Race",
            track_name="Test Track",
            event_date=date.today()
        )
        self.sample_json_content = json.dumps({
            "sessionResult": {
                "leaderBoardLines": [
                    {
                        "currentDriver": {"firstName": "John", "lastName": "Doe"},
                        "car": {"carModel": "Porsche 991 GT3 R", "teamName": "Team Racing", "raceNumber": 1},
                        "timing": {"bestLap": 90500}
                    },
                    {
                        "currentDriver": {"firstName": "Jane", "lastName": "Smith"},
                        "car": {"carModel": "Ferrari 488 GT3", "teamName": "Scuderia", "raceNumber": 2},
                        "timing": {"bestLap": 91200}
                    }
                ]
            }
        })

    def test_parse_acc_results_json(self):
        """Testa se a função de parsing cria os objetos corretamente."""
        self.assertEqual(Driver.objects.count(), 0)
        self.assertEqual(Team.objects.count(), 0)
        self.assertEqual(RaceResult.objects.count(), 0)

        # Chama a função de parsing
        result = parse_acc_results_json(self.sample_json_content, self.event)
        
        # Verifica o resultado
        self.assertEqual(result.get("success"), "2 resultados processados.")
        self.assertEqual(Driver.objects.count(), 2)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(RaceResult.objects.count(), 2)

        # Verifica os detalhes do primeiro resultado
        driver1 = Driver.objects.get(full_name="John Doe")
        team1 = Team.objects.get(name="Team Racing")
        race_result1 = RaceResult.objects.get(driver=driver1)

        self.assertEqual(race_result1.event, self.event)
        self.assertEqual(race_result1.team, team1)
        self.assertEqual(race_result1.car_model, "Porsche 991 GT3 R")
        self.assertEqual(race_result1.final_position, 1)
        self.assertEqual(race_result1.best_lap_time.total_seconds(), 90.5)

        # Verifica se o piloto foi associado à equipe
        self.assertEqual(driver1.team, team1)

class ViewsTestCase(TestCase):
    def setUp(self):
        """Prepara dados para os testes das views."""
        self.event = Event.objects.create(
            name="Another Test Race",
            track_name="Another Test Track",
            event_date=date.today()
        )
        self.upload_url = reverse('upload_result')

    def test_upload_view_get(self):
        """Testa se a página de upload é renderizada corretamente."""
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'league_manager/upload_result.html')

    def test_upload_view_post_success(self):
        """Testa o upload bem-sucedido de um arquivo JSON."""
        json_content = json.dumps({
            "sessionResult": {"leaderBoardLines": [{"currentDriver": {"firstName": "Test", "lastName": "Driver"}, "car": {"raceNumber": 1}}]}
        })
        json_file = SimpleUploadedFile("result.json", json_content.encode('utf-8'), content_type="application/json")
        
        data = {'event': self.event.id, 'file': json_file}
        response = self.client.post(self.upload_url, data, follow=True)
        
        # Verifica se foi redirecionado para a página correta
        self.assertRedirects(response, reverse('team_list'))
        # Verifica se a mensagem de sucesso foi exibida
        self.assertContains(response, "1 resultados processados.")
        # Verifica se o resultado foi criado no banco
        self.assertTrue(RaceResult.objects.exists())

    def test_upload_view_post_invalid_json(self):
        """Testa o upload de um arquivo JSON inválido."""
        invalid_json_content = "isso não é um json"
        json_file = SimpleUploadedFile("result.json", invalid_json_content.encode('utf-8'), content_type="application/json")
        
        data = {'event': self.event.id, 'file': json_file}
        response = self.client.post(self.upload_url, data, follow=True)
        
        self.assertRedirects(response, reverse('team_list'))
        self.assertContains(response, "Arquivo JSON inválido.")
        self.assertFalse(RaceResult.objects.exists())

    def test_league_standings_view(self):
        """Testa se a classificação da liga é calculada e ordenada corretamente."""
        # Cria pilotos e resultados
        d1 = Driver.objects.create(full_name="Piloto 1")
        d2 = Driver.objects.create(full_name="Piloto 2")
        d3 = Driver.objects.create(full_name="Piloto 3") # Piloto sem pontos
        
        RaceResult.objects.create(event=self.event, driver=d1, final_position=1, points_earned=25)
        RaceResult.objects.create(event=self.event, driver=d2, final_position=2, points_earned=18)
        # Piloto 1 corre de novo em outro evento
        event2 = Event.objects.create(name="Event 2", track_name="Track 2", event_date=date.today())
        RaceResult.objects.create(event=event2, driver=d1, final_position=3, points_earned=15)
        
        # Acessa a página de classificação
        response = self.client.get(reverse('league_standings'))
        self.assertEqual(response.status_code, 200)

        # Verifica a ordem e os totais de pontos
        # Esperado: Piloto 1 (40 pontos), Piloto 2 (18 pontos)
        # O Piloto 3 não deve aparecer pois não tem pontos.
        standings = list(response.context['standings'])
        self.assertEqual(len(standings), 2)
        
        # Verifica o primeiro colocado
        self.assertEqual(standings[0], d1)
        self.assertEqual(standings[0].total_points, 40)

        # Verifica o segundo colocado
        self.assertEqual(standings[1], d2)
        self.assertEqual(standings[1].total_points, 18)
