from django.urls import path
from . import views

app_name = 'paif'

urlpatterns = [
    # Páginas principais
    path('', views.index, name='index'),
    path('listar/', views.paif_listar, name='paif_listar'),
    path('novo/', views.paif_novo, name='paif_novo'),
    
    # Cadastro e edição de fichas
    path('cadastro/novo/', views.paif_cadastro, name='paif_cadastro_novo'),
    path('cadastro/<int:id>/', views.paif_cadastro, name='paif_cadastro'),
    path('cadastro/<int:id>/<str:modo>/', views.paif_cadastro, name='paif_cadastro'),
    
    # Páginas individuais que também podem ser acessadas diretamente
    path('fichainscricao/', views.paif_fichainscricao, name='paif_fichainscricao'),
    path('fichainscricao/<int:id>/', views.paif_fichainscricao, name='paif_fichainscricao'),
    path('fichainscricao/<int:id>/<str:modo>/', views.paif_fichainscricao, name='paif_fichainscricao'),
    path('evolucao/', views.paif_evolucao, name='paif_evolucao'),
    path('evolucao/<int:id>/', views.paif_evolucao, name='paif_evolucao'),
    
    # APIs
    path('api/verificar-numero-paif/', views.verificar_numero_paif, name='verificar_numero_paif'),
    path('api/ficha-adicionar/', views.api_ficha_adicionar, name='api_ficha_adicionar'),
    path('api/ficha-atualizar/', views.api_ficha_atualizar, name='api_ficha_atualizar'),
    path('api/evolucao-adicionar/', views.api_evolucao_adicionar, name='api_evolucao_adicionar'),
    path('api/membros-familiares-adicionar/', views.api_membros_familiares_adicionar, name='api_membros_familiares_adicionar'),
    
    path('ficha/<int:id>/pdf/', views.exportar_ficha_pdf, name='exportar_ficha_pdf'),
]
