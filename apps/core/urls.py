from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Rotas específicas para recepção
    path('recepcao/', views.recepcao_view, name='recepcao'),
    path('recepcao/busca/', views.recepcao_busca, name='recepcao_busca'),
    path('recepcao/agendamento/', views.recepcao_agendamento, name='recepcao_agendamento'),
]
