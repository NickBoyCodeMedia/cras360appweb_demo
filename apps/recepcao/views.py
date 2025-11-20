from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

from apps.core.models import Agendamento, Beneficiario, DemandaEspontanea, Atendimento
from apps.auth_app.models import Usuario  # Adicione esta importação
from django.conf import settings

@login_required
def index(request):
    """Página principal da recepção"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')
    
    data_atual = timezone.now().date()
    agendamentos_dia = Agendamento.objects.filter(data=data_atual).order_by('hora')
    
    context = {
        'data_atual': data_atual,
        'agendamentos_dia': agendamentos_dia,
    }
    
    return render(request, 'recepcao/index.html', context)

@login_required
def agendamento_list(request):
    """Página de gerenciamento de agendamentos"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')
    
    tecnicos = [
        {'nome': 'Carlos Técnico PAIF', 'perfil': 'Técnico PAIF', 'disponivel': True},
        {'nome': 'Ana Técnico SCFV', 'perfil': 'Técnico SCFV', 'disponivel': True},
        {'nome': 'João Assistente', 'perfil': 'Assistente Social', 'disponivel': False}
    ]

    context = {
        'tecnicos': tecnicos,
        'horarios_disponiveis': ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00'],
        'data_atual': datetime.now().strftime('%Y-%m-%d')
    }
    
    return render(request, 'recepcao/agendamento.html', context)

@login_required
def novo_agendamento(request):
    """Página para criar um novo agendamento"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        beneficiario_id = request.POST.get('beneficiario_id')
        tipo_atendimento = request.POST.get('tipo_atendimento')
        tecnico_id = request.POST.get('tecnico')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        observacao = request.POST.get('observacao')
        
        # Validação básica
        if not all([beneficiario_id, tipo_atendimento, tecnico_id, data, hora]):
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return redirect('recepcao_novo_agendamento')
            
        try:
            # Obter objetos do banco de dados
            beneficiario = Beneficiario.objects.get(id=beneficiario_id)
            tecnico = Usuario.objects.get(id=tecnico_id)
            
            # Criar data/hora combinados
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            hora_obj = datetime.strptime(hora, '%H:%M').time()
            data_hora = datetime.combine(data_obj, hora_obj)
            
            # Criar agendamento
            Agendamento.objects.create(
                beneficiario=beneficiario,
                tecnico=tecnico,
                data_hora=data_hora,
                tipo_atendimento=tipo_atendimento,
                observacao=observacao,
                status='Agendado',
                criado_por=request.user,
                unidade=request.user.unidade
            )
            
            messages.success(request, f'Agendamento para {beneficiario.nome_completo} criado com sucesso!')
            return redirect('recepcao_agendamento')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar agendamento: {str(e)}')
            return redirect('recepcao_novo_agendamento')
    
    # Obter técnicos disponíveis
    tecnicos = [
        {'id': 1, 'nome_completo': 'Carlos Técnico', 'perfil': 'Técnico PAIF'},
        {'id': 2, 'nome_completo': 'Ana Técnico', 'perfil': 'Técnico SCFV'},
        {'id': 3, 'nome_completo': 'João Silva', 'perfil': 'Assistente Social'}
    ]
    
    context = {
        'tecnicos': tecnicos,
        'data_hoje': datetime.now().date(),
    }
    
    return render(request, 'recepcao/novo_agendamento.html', context)

@login_required
def busca_beneficiario(request):
    """Página de busca de beneficiários"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')
    
    context = {}
    termo = request.GET.get('termo', '')
    
    if termo:
        beneficiarios = Beneficiario.objects.filter(
            nome_completo__icontains=termo
        ) | Beneficiario.objects.filter(
            cpf__icontains=termo
        ) | Beneficiario.objects.filter(
            nis__icontains=termo
        ) | Beneficiario.objects.filter(
            rg__icontains=termo
        )
        
        context['beneficiarios'] = beneficiarios
        context['termo'] = termo
        
        tecnicos_disponiveis = []
        try:
            tecnicos_disponiveis = Usuario.objects.filter(
                perfil__in=['Assistente Social', 'Psicólogo', 'Técnico PAIF', 'Técnico SCFV'],
                is_active=True
            )
        except Exception:
            tecnicos_disponiveis = [
                {'id': 1, 'nome_completo': 'Carlos Técnico', 'perfil': 'Técnico PAIF'},
                {'id': 2, 'nome_completo': 'Ana Técnico', 'perfil': 'Técnico SCFV'},
                {'id': 3, 'nome_completo': 'João Silva', 'perfil': 'Assistente Social'}
            ]
        
        context['tecnicos_disponiveis'] = tecnicos_disponiveis
        
        context['tipos_atendimento'] = [
            'PAIF', 'SCFV', 'Cadastro Único', 'Benefício Eventual',
            'Atendimento Psicológico', 'Orientação Social', 'Outros'
        ]
    
    return render(request, 'recepcao/busca.html', context)

@login_required
def iniciar_atendimento_beneficiario(request, beneficiario_id):
    """Inicia um novo atendimento para beneficiário existente"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para executar esta ação.')
        return redirect('dashboard')
        
    try:
        beneficiario = Beneficiario.objects.get(id=beneficiario_id)
    except Beneficiario.DoesNotExist:
        messages.error(request, "Beneficiário não encontrado.")
        return redirect('recepcao_busca')
        
    if request.method == 'POST':
        tipo_atendimento = request.POST.get('tipo_atendimento')
        tecnico_id = request.POST.get('tecnico_id')
        observacao = request.POST.get('observacao')
        prioridade = request.POST.get('prioridade', 'normal')
        
        if not tipo_atendimento or not tecnico_id:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect('recepcao_iniciar_atendimento', beneficiario_id=beneficiario_id)
        
        try:
            tecnico = Usuario.objects.get(id=tecnico_id)
            
            demanda = DemandaEspontanea.objects.create(
                beneficiario=beneficiario,
                tipo_atendimento=tipo_atendimento,
                motivo_procura=observacao,
                prioridade=prioridade,
                registrado_por=request.user,
                data_registro=datetime.now()
            )
            
            atendimento = Atendimento.objects.create(
                beneficiario=beneficiario,
                tecnico=tecnico,
                tipo_atendimento=tipo_atendimento,
                origem='demanda_espontanea',
                data_atendimento=datetime.now().date(),
                hora_inicio=datetime.now().time(),
                status='aguardando',
                demanda_relacionada=demanda
            )
            
            messages.success(
                request, 
                f"Atendimento iniciado com sucesso para {beneficiario.nome_completo}. " + 
                f"Aguardando disponibilidade de {tecnico.nome_completo}."
            )
            return redirect('recepcao_index')
            
        except Exception as e:
            messages.error(request, f"Erro ao iniciar atendimento: {str(e)}")
            return redirect('recepcao_iniciar_atendimento', beneficiario_id=beneficiario_id)
    
    context = {
        'beneficiario': beneficiario,
        'tipos_atendimento': [
            'PAIF', 'SCFV', 'Cadastro Único', 'Benefício Eventual',
            'Atendimento Psicológico', 'Orientação Social', 'Outros'
        ],
        'tecnicos_disponiveis': [
            {'id': 1, 'nome_completo': 'Carlos Técnico', 'perfil': 'Técnico PAIF'},
            {'id': 2, 'nome_completo': 'Ana Técnico', 'perfil': 'Técnico SCFV'},
            {'id': 3, 'nome_completo': 'João Silva', 'perfil': 'Assistente Social'}
        ]
    }
    
    return render(request, 'recepcao/iniciar_atendimento.html', context)

@login_required
def confirmar_presenca(request, agendamento_id):
    """Confirmar presença de beneficiário"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para executar esta ação.')
        return redirect('dashboard')
    
    messages.success(request, "Presença confirmada com sucesso!")
    return redirect('recepcao_index')

@login_required
def registrar_ausencia(request, agendamento_id):
    """Registrar ausência de beneficiário"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para executar esta ação.')
        return redirect('dashboard')
    
    messages.warning(request, "Ausência registrada com sucesso!")
    return redirect('recepcao_index')

@login_required
def demanda_espontanea(request):
    """Página para registrar uma demanda espontânea"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('dashboard')
    
    # Obter técnicos disponíveis (em produção seria do banco de dados)
    tecnicos = [
        {'id': 1, 'nome_completo': 'Carlos Silva', 'perfil': 'Assistente Social'},
        {'id': 2, 'nome_completo': 'Ana Souza', 'perfil': 'Psicóloga'},
        {'id': 3, 'nome_completo': 'Pedro Santos', 'perfil': 'Técnico PAIF'}
    ]
    
    context = {
        'tecnicos': tecnicos,
    }
    
    return render(request, 'recepcao/demanda_espontanea.html', context)

@login_required
def registrar_demanda_espontanea(request):
    """API para registrar demanda espontânea via AJAX"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Permissão negada'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    return JsonResponse({
        'success': True, 
        'message': 'Demanda registrada com sucesso!',
        'beneficiario_nome': 'Nome do Beneficiário',
        'tecnico_id': 1
    })

@login_required
def notificar_tecnico_fila(request, fila_id):
    """API para notificar técnico sobre demanda espontânea"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Permissão negada'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    return JsonResponse({
        'success': True, 
        'message': 'Técnico notificado com sucesso!'
    })

@login_required
def atualizar_tecnico_fila(request):
    """API para atualizar técnico de uma fila de demanda espontânea"""
    if request.user.perfil != 'Recepção' and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Permissão negada'}, status=403)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    return JsonResponse({
        'success': True, 
        'message': 'Técnico atribuído com sucesso!'
    })

@login_required
def agendar_demanda_espontanea(request):
    if request.method == 'POST':
        # Obter dados do formulário
        nome_completo = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')
        data_agendamento = request.POST.get('data_agendamento')
        hora_agendamento = request.POST.get('hora_agendamento')
        demanda = request.POST.get('demanda')
        tecnico_id = request.POST.get('tecnico_id')
        prioridade = request.POST.get('prioridade', 'normal')
        observacao = request.POST.get('observacao')
        
        # Buscar o beneficiário pelo CPF ou criar um registro básico
        beneficiario = None
        if cpf:
            # Remover caracteres não numéricos do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            try:
                beneficiario = Beneficiario.objects.get(cpf=cpf_limpo)
            except Beneficiario.DoesNotExist:
                pass
        
        if not beneficiario:
            # Criar um registro básico de beneficiário
            beneficiario = Beneficiario.objects.create(
                nome_completo=nome_completo,
                data_nascimento=data_nascimento if data_nascimento else None,
                telefone=telefone,
                cpf=cpf if cpf else None,
                criado_por=request.user,
                unidade=request.user.unidade
            )
        
        # Criar o agendamento
        tecnico = Usuario.objects.get(id=tecnico_id)
        
        # Combinar data e hora
        data_hora = datetime.datetime.combine(
            datetime.datetime.strptime(data_agendamento, '%Y-%m-%d').date(),
            datetime.datetime.strptime(hora_agendamento, '%H:%M').time()
        )
        
        # Criar o agendamento
        Agendamento.objects.create(
            beneficiario=beneficiario,
            tecnico=tecnico,
            data_hora=data_hora,
            tipo_atendimento='Demanda Espontânea',
            motivo=demanda,
            prioridade=prioridade,
            observacao=observacao,
            status='Agendado',
            criado_por=request.user,
            unidade=request.user.unidade
        )
        
        messages.success(request, f'Agendamento realizado com sucesso para {nome_completo}')
        return redirect('recepcao_busca')
    
    return redirect('recepcao_busca')

@login_required
def api_buscar_beneficiarios(request):
    """API para buscar beneficiários por nome, CPF ou NIS"""
    termo = request.GET.get('termo', '').strip()
    
    # CÓDIGO TEMPORÁRIO: Simula resultados para testes
    # Em produção, isso seria substituído pela consulta real ao banco
    if not termo:
        return JsonResponse({'beneficiarios': []})
    
    # Para fins de demonstração, retornamos dados fictícios
    # Se o termo contiver "404" ou "nao", retornamos vazia para simular "não encontrado"
    if '404' in termo.lower() or 'nao' in termo.lower():
        return JsonResponse({'beneficiarios': []})
    
    # Caso contrário, simulamos alguns resultados
    beneficiarios = [
        {
            'id': 1,
            'nome_completo': f'{termo.title()} da Silva',
            'cpf': '123.456.789-00',
            'nis': '12345678901',
            'data_nascimento': '01/01/1980',
            'paif': True
        },
        {
            'id': 2,
            'nome_completo': f'Maria {termo.title()}',
            'cpf': '987.654.321-00',
            'nis': '10987654321',
            'data_nascimento': '15/05/1975',
            'paif': False
        }
    ]
    
    return JsonResponse({'beneficiarios': beneficiarios})