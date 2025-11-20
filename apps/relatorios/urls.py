from django.urls import path
from . import views

app_name = 'relatorios'  # Esta linha é crucial para o namespace funcionar

urlpatterns = [
    # Páginas principais de relatórios
    path('', views.index, name='index'),
    path('scfv/', views.scfv_index, name='scfv'),
    path('paif/', views.paif_index, name='paif'),
    
    # APIs para obter dados dos relatórios
    path('api/scfv/', views.api_scfv, name='api_scfv'),
    path('api/paif/', views.api_paif, name='api_paif'),
    
    # Nova API para verificação de permissões
    path('verificar-permissao/<str:tipo_relatorio>/', views.verificar_permissao_ajax, name='verificar_permissao'),
    
    # Nova URL para depuração de permissões
    path('debug-permissoes/', views.debug_permissoes, name='debug_permissoes'),
    
    # Exportação de relatórios
    path('exportar/<str:tipo>/<str:formato>/', views.exportar_relatorio, name='exportar'),
    
    # Fichas de cadastro
    path('scfv/ficha-cadastro/<int:id>/', views.scfv_ficha_cadastro, name='scfv_ficha_cadastro'),
    path('paif/ficha-cadastro/<int:id>/', views.paif_ficha_cadastro, name='paif_ficha_cadastro'),
    
    # Geração de relatórios
    path('scfv/gerar/', views.gerar_scfv, name='gerar_scfv'),
    path('paif/gerar/', views.gerar_paif, name='gerar_paif'),
]
