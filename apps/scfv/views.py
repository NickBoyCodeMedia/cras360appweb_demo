from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

def index(request):
    """Página inicial do módulo SCFV"""
    return render(request, 'scfv_index.html')

def jovem_novo(request):
    """Formulário para novo cadastro de SCFV Infantojuvenil"""
    context = {
        'modo': 'novo',
        'data_atual': datetime.now().strftime('%d/%m/%Y')
    }
    return render(request, 'scfv_jovem.html', context)

def idoso_novo(request):
    """Formulário para novo cadastro de SCFV Idosos"""
    context = {
        'data_atual': datetime.now().strftime('%d/%m/%Y')
    }
    return render(request, 'scfv_idoso.html', context)

def salvar(request):
    """Salvar dados do formulário SCFV (tanto jovem quanto idoso)"""
    if request.method == 'POST':
        # Aqui seria a lógica para salvar os dados
        # Por enquanto, apenas simular sucesso
        messages.success(request, "Cadastro salvo com sucesso!")
        return redirect('scfv:index')
    return redirect('scfv:index')

def editar(request, id):
    """Editar um cadastro SCFV existente"""
    # Simulação de dados para o template
    dados = {
        'nome_crianca': 'NOME EXEMPLO',
        'data_nascimento': '01/01/2010',
        # Outros campos viriam do banco de dados
    }
    context = {
        'modo': 'editar',
        'id': id,
        'dados': dados,
        'data_atual': datetime.now().strftime('%d/%m/%Y')
    }
    return render(request, 'scfv_jovem.html', context)

def atualizar(request, id):
    """Atualizar dados de um cadastro SCFV"""
    if request.method == 'POST':
        # Aqui seria a lógica para atualizar
        messages.success(request, "Cadastro atualizado com sucesso!")
        return redirect('scfv:consulta')
    return redirect('scfv:index')

def consulta(request):
    """Página de consulta de cadastros SCFV"""
    # Implementação futura
    return render(request, 'scfv_consulta.html')
