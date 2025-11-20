from django.urls import path
from . import views

app_name = 'gestao'

urlpatterns = [
    path('', views.gestao_municipal, name='gestao_municipal'),
    path('cras/<int:cras_id>/', views.detalhe_cras, name='detalhe_cras'),
]