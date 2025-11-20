from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Q
from apps.core.models import Cidade, CRAS, FichaPAIF, Beneficiario, Atendimento
from datetime import datetime, timedelta

def user_in_gestores_group(user):
    """Verifica se o usuário pertence ao grupo de gestores ou é superusuário"""
    return user.groups.filter(name='gestores').exists() or user.is_superuser

@login_required
@user_passes_test(user_in_gestores_group, login_url='login')
def gestao_municipal(request):
    """View para a página de gestão municipal de CRAS"""
    # Definir período padrão (último mês)
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    fim_mes = hoje
    
    # Verificar se há filtro de cidade na requisição
    cidade_id = request.GET.get('cidade')
    if cidade_id:
        cidade = Cidade.objects.filter(id=cidade_id).first()
    else:
        # Para admin global, mostrar Breves como padrão ou a primeira cidade
        cidade = Cidade.objects.filter(nome='Breves', uf='PA').first() or Cidade.objects.first()
    
    if not cidade:
        messages.error(request, "Nenhuma cidade encontrada no sistema")
        return redirect('dashboard')
    
    # Obter todos os CRAS da cidade selecionada
    lista_cras = CRAS.objects.filter(cidade=cidade)
    
    # Calcular métricas para estatísticas
    total_familias = FichaPAIF.objects.filter(cras__in=lista_cras).count()
    
    # Estatísticas por CRAS
    cras_estatisticas = []
    for cras in lista_cras:
        familias = FichaPAIF.objects.filter(cras=cras).count()
        beneficiarios = Beneficiario.objects.filter(cras=cras).count()
        
        # Atendimentos no último mês
        atendimentos = Atendimento.objects.filter(
            beneficiario__cras=cras,
            data_atendimento__range=(inicio_mes, fim_mes)
        ).count()
        
        # Definir status baseado em alguma métrica
        if atendimentos > 100:
            status = 'normal'
        elif atendimentos > 50:
            status = 'atencao'
        else:
            status = 'critico'
        
        cras_estatisticas.append({
            'id': cras.id,
            'nome': cras.nome,
            'endereco': cras.endereco,
            'coordenador': cras.coordenador,
            'familias_cadastradas': familias,
            'atendimentos_mes': atendimentos,
            'status': status
        })
    
    # Exemplos simplificados para outras métricas
    # Na implementação real, você obteria esses dados do banco corretamente
    total_visitas = 489  # Implementar consulta real
    total_inclusoes = 157  # Implementar consulta real
    total_oficinas = 25   # Implementar consulta real
    
    # Dados de alertas e eventos (exemplos)
    alertas = [
        {'mensagem': 'Alto volume de atendimentos sem agendamento', 'cras': 'CRAS Cidade Nova', 'data': '21/04/2025'},
        {'mensagem': 'Mais de 15 dias sem atualização do CadÚnico', 'cras': 'CRAS Riacho Doce', 'data': '19/04/2025'}
    ]
    
    eventos = [
        {'titulo': 'Oficina de Artesanato para Idosos', 'data': '30/04/2025', 'cras': 'CRAS Santa Cruz'},
        {'titulo': 'Palestra sobre Direitos Sociais', 'data': '03/05/2025', 'cras': 'CRAS Jardim Tropical'},
        {'titulo': 'Reunião de Avaliação Trimestral', 'data': '10/05/2025', 'cras': 'Todos os CRAS'}
    ]
    
    context = {
        'cidade': cidade,
        'lista_cras': cras_estatisticas,
        'total_familias': total_familias,
        'total_visitas': total_visitas,
        'total_inclusoes': total_inclusoes,
        'total_oficinas': total_oficinas,
        'alertas': alertas,
        'eventos': eventos,
    }
    
    return render(request, 'gestao/gestao.html', context)

@login_required
@user_passes_test(user_in_gestores_group, login_url='login')
def detalhe_cras(request, cras_id):
    """View para exibir detalhes de um CRAS específico"""
    try:
        cras = CRAS.objects.get(id=cras_id)
    except CRAS.DoesNotExist:
        messages.error(request, "CRAS não encontrado")
        return redirect('gestao:gestao_municipal')
    
    # Obter estatísticas do CRAS
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)
    fim_mes = hoje
    
    # Contagens e estatísticas
    familias = FichaPAIF.objects.filter(cras=cras).count()
    beneficiarios = Beneficiario.objects.filter(cras=cras).count()
    
    # Atendimentos no último mês
    atendimentos = Atendimento.objects.filter(
        beneficiario__cras=cras,
        data_atendimento__range=(inicio_mes, fim_mes)
    ).count()
    
    # Exemplos de outros dados que podem ser úteis
    ultimos_atendimentos = Atendimento.objects.filter(
        beneficiario__cras=cras
    ).order_by('-data_atendimento')[:10]
    
    context = {
        'cras': cras,
        'familias': familias,
        'beneficiarios': beneficiarios,
        'atendimentos': atendimentos,
        'ultimos_atendimentos': ultimos_atendimentos,
    }
    
    return render(request, 'gestao/detalhe_cras.html', context)