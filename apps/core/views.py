from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
import datetime
import json
from apps.core.models import Cidade, CRAS, FichaPAIF, Beneficiario, Atendimento

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    # Dados exemplo para agendamentos
    data_atual = timezone.now().strftime("%d/%m/%Y")
    
    # Dados comuns para todos os perfis
    context = {
        'data_atual': data_atual,
        'perfil': request.user.perfil,
        'user': request.user,  # Certifique-se de que o usuário está sendo enviado ao template
    }
    
    # Dados específicos por perfil
    if request.user.perfil == 'Recepção':
        # Dados para o perfil de recepção
        agendamentos = [
            {'data': '15/06/2023', 'hora': '09:00', 'nome': 'Maria Silva', 'motivo': 'Atendimento PAIF', 'status': 'Confirmado'},
            {'data': '15/06/2023', 'hora': '10:30', 'nome': 'João Santos', 'motivo': 'Inscrição SCFV', 'status': 'Pendente'},
            {'data': '15/06/2023', 'hora': '14:00', 'nome': 'Ana Oliveira', 'motivo': 'Atualização Cadastral', 'status': 'Confirmado'}
        ]
        context.update({
            'agendamentos': agendamentos,
            'total_agendamentos': len(agendamentos),
            'agendamentos_confirmados': 2,
            'agendamentos_pendentes': 1,
        })
    
    elif request.user.perfil in ['Assistente Social', 'Técnico PAIF']:
        # Dados para Assistente Social e Técnico PAIF
        atendimentos = [
            {'data': '15/06/2023', 'nome': 'Maria Silva', 'tipo': 'PAIF', 'status': 'Concluído'},
            {'data': '16/06/2023', 'nome': 'João Santos', 'tipo': 'Acompanhamento Familiar', 'status': 'Agendado'},
            {'data': '16/06/2023', 'nome': 'Ana Oliveira', 'tipo': 'Visita Domiciliar', 'status': 'Pendente'}
        ]
        context.update({
            'atendimentos': atendimentos,
            'total_atendimentos_pendentes': 2,
            'total_atendimentos_dia': 1,
        })
    
    elif request.user.perfil in ['Técnico SCFV', 'Técnico']:
        # Dados para Técnico SCFV e Técnico Pedagogo
        grupos = [
            {'nome': 'Crianças 6-9 anos', 'horario': '08:00-10:00', 'dia': 'Segunda e Quarta', 'participantes': 15},
            {'nome': 'Adolescentes 14-17 anos', 'horario': '14:00-16:00', 'dia': 'Terça e Quinta', 'participantes': 18},
            {'nome': 'Idosos', 'horario': '09:00-11:00', 'dia': 'Sexta', 'participantes': 12}
        ]
        context.update({
            'grupos': grupos,
            'proximas_atividades': [
                {'grupo': 'Crianças 6-9 anos', 'data': '15/06/2023', 'hora': '08:00', 'atividade': 'Oficina de Artes'},
                {'grupo': 'Adolescentes 14-17 anos', 'data': '16/06/2023', 'hora': '14:00', 'atividade': 'Debate sobre Cidadania'}
            ],
        })
    
    elif request.user.perfil == 'Coordenador':
        # Dados para Coordenador
        # Criar os dados diretamente como listas de dicionários em vez de strings JSON
        distribuicao_publico = [
            {'label': 'Crianças', 'valor': 30},
            {'label': 'Adolescentes', 'valor': 25},
            {'label': 'Adultos', 'valor': 35},
            {'label': 'Idosos', 'valor': 10}
        ]
        
        atendimentos_por_tipo = [
            {'label': 'PAIF', 'valor': 45},
            {'label': 'SCFV', 'valor': 35},
            {'label': 'Benefícios', 'valor': 15},
            {'label': 'Outros', 'valor': 5}
        ]
        
        estatisticas = {
            'familias_atendidas': 145,
            'atendimentos_mes': 130,
            'participantes_scfv': 78,
            'oficinas_ativas': 5,
            'distribuicao_publico': distribuicao_publico,
            'atendimentos_por_tipo': atendimentos_por_tipo
        }
        
        context.update({
            'estatisticas': estatisticas,
            'documentos_pendentes': 3,
            'relatorios_mensais': [
                {'mes': 'Janeiro', 'status': 'Concluído', 'url': '#'},
                {'mes': 'Fevereiro', 'status': 'Concluído', 'url': '#'},
                {'mes': 'Março', 'status': 'Pendente', 'url': '#'}

            ]
        })
    
    elif request.user.perfil == 'Auxiliar Administrativo':
        # Dados para Auxiliar Administrativo
        documentos = [
            {'tipo': 'Ofício', 'numero': '023/2023', 'data': '10/06/2023', 'destinatario': 'Secretaria de Assistência Social'},
            {'tipo': 'Memorando', 'numero': '045/2023', 'data': '12/06/2023', 'destinatario': 'CREAS'},
            {'tipo': 'Declaração', 'numero': '089/2023', 'data': '14/06/2023', 'destinatario': 'Beneficiário'}
        ]
        context.update({
            'documentos': documentos,
            'listas_frequencia': [
                {'nome': 'Grupo Crianças - Junho', 'status': 'Impresso', 'data': '01/06/2023'},
                {'nome': 'Grupo Adolescentes - Junho', 'status': 'Pendente', 'data': '01/06/2023'},
                {'nome': 'Grupo Idosos - Junho', 'status': 'Configuração', 'data': '01/06/2023'}
            ],
            'estoque_itens_baixos': 2
        })
        
    return render(request, 'dashboard.html', context)

@login_required
def recepcao_view(request):
    """View para funções específicas de recepção."""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao pessoal da recepção.')
        return redirect('dashboard')
        
    context = {
        'data_atual': timezone.now().strftime("%d/%m/%Y"),
        'agendamentos_dia': [
            {'hora': '08:00', 'nome': 'João Silva', 'motivo': 'Atendimento PAIF', 'status': 'Confirmado'},
            {'hora': '09:00', 'nome': 'Maria Santos', 'motivo': 'Inscrição SCFV', 'status': 'Pendente'},
            {'hora': '10:30', 'nome': 'José Oliveira', 'motivo': 'Atualização Cadastral', 'status': 'Confirmado'}
        ]
    }
    return render(request, 'recepcao/index.html', context)

@login_required
def recepcao_busca(request):
    """View para busca de beneficiários pela recepção."""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao pessoal da recepção.')
        return redirect('dashboard')
        
    # Código para buscar beneficiários
    context = {
        'termo_busca': request.GET.get('termo', '')
    }
    return render(request, 'recepcao/busca.html', context)

@login_required
def recepcao_agendamento(request):
    """View para criar/gerenciar agendamentos."""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao pessoal da recepção.')
        return redirect('dashboard')
        
    context = {
        'tecnicos': [
            {'nome': 'Carlos Técnico PAIF', 'perfil': 'Técnico PAIF', 'disponivel': True},
            {'nome': 'Ana Técnico SCFV', 'perfil': 'Técnico SCFV', 'disponivel': True},
            {'nome': 'João Assistente', 'perfil': 'Assistente Social', 'disponivel': False}
        ],
        'horarios_disponiveis': ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
    }
    return render(request, 'recepcao/agendamento.html', context)

@login_required
def gestao_municipal(request):
    """View para a página de gestão municipal de CRAS"""
    # Verificar se o usuário tem permissão para acessar a gestão municipal
    if not request.user.is_superuser and request.user.perfil != 'Coordenador':
        messages.error(request, "Você não tem permissão para acessar a gestão municipal.")
        return redirect('dashboard')
        
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
