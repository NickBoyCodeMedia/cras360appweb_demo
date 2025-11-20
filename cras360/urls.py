"""
URL configuration for cras360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Importar views da aplicação core
from apps.core import views as core_views
# Importar de outro aplicativo se necessário
from apps.gestao import views as gestao_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Aplicativos do sistema
    path('', include('apps.core.urls')),  # Rota raiz para o aplicativo principal
    path('paif/', include('apps.paif.urls')),  # Rotas para o aplicativo PAIF
    path('scfv/', include('apps.scfv.urls')),  # Rotas para o aplicativo SCFV
    path('relatorios/', include('apps.relatorios.urls')),  # Rotas para relatórios
    path('tecnico/', include('apps.tecnico.urls')),  # Rotas para técnicos
    path('recepcao/', include('apps.recepcao.urls')),  # Rotas para recepção
    path('gestao/', include('apps.gestao.urls')),  # Rotas para gestão
    # Rotas de autenticação
    path('contas/', include('apps.auth_app.urls')),
]
