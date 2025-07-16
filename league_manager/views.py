from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Team, Driver
from .forms import TeamForm, UploadFileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import parse_acc_results_json
from django.db.models import Sum

class TeamListView(ListView):
    model = Team
    template_name = 'league_manager/team_list.html'
    context_object_name = 'teams'

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'league_manager/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'league_manager/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'league_manager/team_confirm_delete.html'
    success_url = reverse_lazy('team_list')

class LeagueStandingsView(ListView):
    model = Driver
    template_name = 'league_manager/league_standings.html'
    context_object_name = 'standings'

    def get_queryset(self):
        """
        Calcula a pontuação total para cada piloto e ordena-os.
        """
        # Anota cada piloto com a soma dos 'points_earned' de todos os seus resultados.
        # Filtra apenas pilotos que têm pelo menos um resultado com pontos.
        return Driver.objects.annotate(
            total_points=Sum('results__points_earned')
        ).filter(total_points__gt=0).order_by('-total_points')

def upload_result_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.cleaned_data['event']
            json_file = form.cleaned_data['file']
            
            # Lê o conteúdo do arquivo
            json_content = json_file.read().decode('utf-8')
            
            # Chama a função de processamento
            result = parse_acc_results_json(json_content, event)

            if "error" in result:
                messages.error(request, result["error"])
            else:
                messages.success(request, result["success"])

            return redirect('team_list') # Redireciona para uma página de sucesso
    else:
        form = UploadFileForm()
        
    return render(request, 'league_manager/upload_result.html', {'form': form})
