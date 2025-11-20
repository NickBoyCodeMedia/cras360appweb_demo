from django.urls import path
from django.http import HttpResponse

# Função de placeholder para exibir algo enquanto o app não está implementado
def tecnico_index(request):
    return HttpResponse("<h1>Módulo Técnico</h1><p>Esta página está em desenvolvimento.</p>")

app_name = 'tecnico'

urlpatterns = [
    path('', tecnico_index, name='index'),
]
