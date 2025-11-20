from django.urls import path
from . import views

app_name = 'scfv'

urlpatterns = [
    path('', views.index, name='index'),
    path('jovem/novo/', views.jovem_novo, name='jovem_novo'),
    path('idoso/novo/', views.idoso_novo, name='idoso_novo'),
    path('salvar/', views.salvar, name='salvar'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('atualizar/<int:id>/', views.atualizar, name='atualizar'),
    path('consulta/', views.consulta, name='consulta'),
]
