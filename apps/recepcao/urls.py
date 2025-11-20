from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recepcao_index'),
    path('agendamento/', views.agendamento_list, name='recepcao_agendamento'),
    path('novo-agendamento/', views.novo_agendamento, name='recepcao_novo_agendamento'),
    path('busca/', views.busca_beneficiario, name='recepcao_busca'),
    path('atendimento-beneficiario/<int:beneficiario_id>/', views.iniciar_atendimento_beneficiario, name='recepcao_iniciar_atendimento'),
    path('confirmar-presenca/<int:agendamento_id>/', views.confirmar_presenca, name='recepcao_registrar_chegada'),
    path('registrar-ausencia/<int:agendamento_id>/', views.registrar_ausencia, name='recepcao_registrar_ausencia'),
    path('demanda-espontanea/', views.demanda_espontanea, name='recepcao_demanda_espontanea'),
    path('registrar-demanda-espontanea/', views.registrar_demanda_espontanea, name='recepcao_registrar_demanda_espontanea'),
    path('notificar-tecnico/<int:fila_id>/', views.notificar_tecnico_fila, name='recepcao_notificar_tecnico'),
    path('atualizar-tecnico-fila/', views.atualizar_tecnico_fila, name='recepcao_atualizar_tecnico_fila'),
    path('agendar-demanda/', views.agendar_demanda_espontanea, name='recepcao_agendar_demanda'),
    path('api/beneficiarios/buscar/', views.api_buscar_beneficiarios, name='api_buscar_beneficiarios'),
]
