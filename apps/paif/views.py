import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from apps.core.models import FichaPAIF, Beneficiario, CRAS
from .forms import FichaPAIFForm, PesquisaPAIFForm, EvolucaoAtendimentoForm, MembroFamiliarForm

# Função auxiliar para obter um identificador do usuário de forma segura
def get_user_identifier(user):
    # Tentar vários atributos em ordem de preferência
    for attribute in ['nome_completo', 'nome', 'email', 'username', 'id']:
        if hasattr(user, attribute):
            value = getattr(user, attribute)
            if value:  # Garantir que não é None ou string vazia
                return str(value)
    
    # Fallback - usar representação em string do objeto se nada for encontrado
    return str(user)

@login_required
def index(request):
    """Página inicial do módulo PAIF."""
    # Verificar se o usuário tem acesso ao PAIF
    if not request.user.is_superuser and request.user.perfil != 'Assistente Social' and request.user.perfil != 'Coordenador':
        messages.error(request, "Você não tem permissão para acessar o módulo PAIF.")
        return redirect('dashboard')
        
    return render(request, 'paif/index.html')

@login_required
def paif_listar(request):
    """Lista todos os registros do PAIF com filtros."""
    # Inicializar form de pesquisa com dados da requisição
    form = PesquisaPAIFForm(request.GET)
    
    # Inicializar queryset base
    queryset = FichaPAIF.objects.all().order_by('-data')
    
    # Filtrar por CRAS do usuário se não for superusuário
    if not request.user.is_superuser and hasattr(request.user, 'cras') and request.user.cras:
        queryset = queryset.filter(cras=request.user.cras)
    
    # Aplicar filtros da pesquisa
    if form.is_valid():
        numero_paif = form.cleaned_data.get('numero_paif')
        nome = form.cleaned_data.get('nome')
        cpf = form.cleaned_data.get('cpf')
        bairro = form.cleaned_data.get('bairro')
        data_inicial = form.cleaned_data.get('data_inicial')
        data_final = form.cleaned_data.get('data_final')
        cras_id = form.cleaned_data.get('cras')
        
        if numero_paif:
            queryset = queryset.filter(numero_paif__icontains=numero_paif)
        if nome:
            queryset = queryset.filter(nome_referencia__icontains=nome)
        if cpf:
            queryset = queryset.filter(cpf__icontains=cpf)
        if bairro:
            queryset = queryset.filter(bairro__icontains=bairro)
        if data_inicial:
            queryset = queryset.filter(data__gte=data_inicial)
        if data_final:
            queryset = queryset.filter(data__lte=data_final)
        if cras_id:
            queryset = queryset.filter(cras_id=cras_id)
    
    # Paginação dos resultados
    pagina = request.GET.get('pagina', 1)
    paginador = Paginator(queryset, 20)  # 20 registros por página
    registros = paginador.get_page(pagina)
    
    context = {
        'form': form,
        'registros': registros,
        'pagina': int(pagina),
        'total_paginas': paginador.num_pages,
        'total_registros': queryset.count()
    }
    return render(request, 'paif/paif_listagem.html', context)

@login_required
def paif_novo(request):
    """Redireciona para a criação de um novo registro PAIF."""
    # Redireciona para cadastro sem ID
    return redirect('paif:paif_cadastro_novo')

@login_required
def paif_cadastro(request, id=None, modo=None):
    """Interface principal com abas para gestão de registro PAIF."""
    # Obter identificador do usuário de forma segura
    usuario_atual = get_user_identifier(request.user)
    
    # Determinar nome técnico adequadamente
    if hasattr(request.user, 'nome_completo') and request.user.nome_completo:
        nome_tecnico = request.user.nome_completo
    elif hasattr(request.user, 'first_name') and request.user.first_name:
        nome_tecnico = f"{request.user.first_name} {request.user.last_name}".strip()
    else:
        nome_tecnico = request.user.username
    
    # Obter valor do parâmetro numero_paif da URL, se existir
    numero_paif_valor = request.GET.get('numero_paif', '')
    
    # Dados da ficha (buscar do banco de dados)
    ficha = None
    if id:
        ficha = get_object_or_404(FichaPAIF, id=id)
    
    # Obter CRAS atual do usuário
    cras_atual = None
    if hasattr(request.user, 'cras') and request.user.cras:
        cras_atual = request.user.cras.nome
    else:
        # Buscar o primeiro CRAS disponível como fallback
        primeiro_cras = CRAS.objects.first()
        if primeiro_cras:
            cras_atual = primeiro_cras.nome

    # Obter histórico de evoluções
    evolucoes = []
    if ficha:
        # Aqui você buscaria as evoluções reais do banco de dados
        # Este é um exemplo simulado
        pass
        
    # Unificar contexto para ambos os templates
    context = {
        'registro_id': id,
        'modo': modo,
        'ficha': ficha,
        'usuario_atual': usuario_atual,
        'data_atual': timezone.now(),
        'nome_tecnico': nome_tecnico,
        'cras_atual': cras_atual,
        'numero_paif_valor': numero_paif_valor,
        'registros_historico': evolucoes,
    }
    
    return render(request, 'paif/paif_abas.html', context)

@login_required
def paif_fichainscricao(request, id=None, modo=None):
    """Exibe e gerencia a ficha de inscrição PAIF."""
    # Obter identificador do usuário de forma segura
    usuario_atual = get_user_identifier(request.user)
    
    # Obter valor do parâmetro numero_paif da URL, se existir
    numero_paif_valor = request.GET.get('numero_paif', '')
    
    # Obter CRAS atual do usuário
    cras_atual = None
    if hasattr(request.user, 'cras') and request.user.cras:
        cras_atual = request.user.cras.nome
    else:
        # Buscar o primeiro CRAS disponível como fallback
        primeiro_cras = CRAS.objects.first()
        if primeiro_cras:
            cras_atual = primeiro_cras.nome
    
    context = {
        'ficha': None,
        'usuario_atual': usuario_atual,
        'data_atual': timezone.now(),
        'cras_atual': cras_atual,
        'numero_paif_valor': numero_paif_valor,
        'em_iframe': True,
    }
    
    if id:
        ficha = get_object_or_404(FichaPAIF, id=id)
        context['ficha'] = ficha
    
    response = render(request, 'paif/paif_fichainscricao.html', context)
    # Garantir que a página possa ser carregada em iframes do mesmo domínio
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@login_required
def paif_evolucao(request, id=None):
    """Exibe e gerencia a evolução de atendimento."""
    # Verificar se o usuário tem permissão para acessar evoluções
    if not request.user.is_superuser and request.user.perfil != 'Assistente Social' and request.user.perfil != 'Coordenador':
        messages.error(request, "Você não tem permissão para acessar evolução de atendimento.")
        return redirect('paif:index')
        
    # Obter o nome completo do usuário de forma segura
    if hasattr(request.user, 'nome_completo') and request.user.nome_completo:
        nome_tecnico = request.user.nome_completo
    elif hasattr(request.user, 'first_name') and request.user.first_name:
        nome_tecnico = f"{request.user.first_name} {request.user.last_name}".strip()
    else:
        nome_tecnico = request.user.username
        
    # Obter CRAS atual do usuário
    cras_atual = None
    if hasattr(request.user, 'cras') and request.user.cras:
        cras_atual = request.user.cras.nome
    else:
        # Buscar o primeiro CRAS disponível como fallback
        primeiro_cras = CRAS.objects.first()
        if primeiro_cras:
            cras_atual = primeiro_cras.nome
            
    # Buscar ficha PAIF se o ID foi fornecido
    ficha = None
    evolucoes = []
    
    if id:
        ficha = get_object_or_404(FichaPAIF, id=id)
        # Aqui você buscaria as evoluções reais do banco de dados
        # Este é um exemplo simulado - implemente conforme seu modelo de evolução
        evolucoes_json = json.dumps([
            {
                'id': 1,
                'data': timezone.now().strftime("%d/%m/%Y"),
                'tecnico': nome_tecnico,
                'cras': cras_atual,
                'descricao': 'Atendimento inicial da família. Realizado cadastro e orientações sobre programas sociais.'
            }
        ])
    else:
        evolucoes_json = '[]'
    
    context = {
        'ficha': ficha,
        'data_atual': timezone.now().strftime("%d/%m/%Y"),
        'nome_tecnico': nome_tecnico,
        'cras': cras_atual,
        'dados_backend': {
            'evolucoes': evolucoes_json
        }
    }
    
    # Adicionar os dados de backend como JSON para o JavaScript
    context['dados_backend'] = json.dumps(context['dados_backend'])
    
    response = render(request, 'paif/paif_evolucao.html', context)
    # Garantir que a página possa ser carregada em iframes do mesmo domínio
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response

@csrf_exempt
def verificar_numero_paif(request):
    """API para verificar se um número PAIF já existe."""
    if request.method == 'POST':
        data = json.loads(request.body)
        numero_paif = data.get('numero_paif')
        
        # Verificar se o número já existe no banco
        existe = FichaPAIF.objects.filter(numero_paif=numero_paif).exists()
        
        return JsonResponse({
            'disponivel': not existe,
            'numero': numero_paif
        })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_ficha_adicionar(request):
    """API para adicionar nova ficha PAIF."""
    if request.method == 'POST':
        # Processar dados do formulário
        dados = request.POST.dict()
        
        # Remover campos vazios
        for key in list(dados.keys()):
            if not dados[key]:
                dados.pop(key)
                
        # Adicionar CRAS do usuário ou primeiro CRAS disponível
        if hasattr(request.user, 'cras') and request.user.cras:
            dados['cras'] = request.user.cras.id
        else:
            primeiro_cras = CRAS.objects.first()
            if primeiro_cras:
                dados['cras'] = primeiro_cras.id
        
        try:
            # Criar nova ficha PAIF
            form = FichaPAIFForm(dados)
            if form.is_valid():
                ficha = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Ficha adicionada com sucesso',
                    'ficha_id': ficha.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Dados inválidos',
                    'errors': form.errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_ficha_atualizar(request):
    """API para atualizar ficha PAIF existente."""
    if request.method == 'POST':
        # Processar dados do formulário
        dados = request.POST.dict()
        ficha_id = dados.get('ficha_id')
        
        if not ficha_id:
            return JsonResponse({
                'success': False,
                'message': 'ID da ficha não fornecido'
            })
            
        # Remover campos vazios
        for key in list(dados.keys()):
            if not dados[key]:
                dados.pop(key)
        
        try:
            # Buscar a ficha existente
            ficha = get_object_or_404(FichaPAIF, id=ficha_id)
            
            # Atualizar ficha
            form = FichaPAIFForm(dados, instance=ficha)
            if form.is_valid():
                ficha = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Ficha atualizada com sucesso'
                })
            else:
                # Retornar detalhes de erros específicos
                error_details = {}
                for field, errors in form.errors.items():
                    error_details[field] = [str(e) for e in errors]
                
                return JsonResponse({
                    'success': False,
                    'message': 'Dados inválidos',
                    'errors': error_details
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_evolucao_adicionar(request):
    """API para adicionar evolução de atendimento."""
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            
            # Validar dados
            form = EvolucaoAtendimentoForm(dados)
            if not form.is_valid():
                return JsonResponse({
                    'success': False,
                    'message': 'Dados inválidos',
                    'errors': form.errors
                })
            
            # Buscar ficha PAIF pelo número
            numero_paif = form.cleaned_data.get('numero_paif')
            try:
                ficha = FichaPAIF.objects.get(numero_paif=numero_paif)
            except FichaPAIF.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Ficha PAIF {numero_paif} não encontrada'
                })
            
            # Criar nova evolução
            # Implementar conforme seu modelo de evolução
            # Exemplo: Evolucao.objects.create(...)
            
            return JsonResponse({
                'success': True,
                'message': 'Evolução adicionada com sucesso',
                'evolucao': {
                    'id': 999,  # ID fictício - substitua pelo ID real
                    'data': form.cleaned_data['data_atendimento'].strftime("%d/%m/%Y"),
                    'tecnico': form.cleaned_data['tecnico'],
                    'cras': form.cleaned_data['cras'],
                    'descricao': form.cleaned_data['descricao']
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def api_membros_familiares_adicionar(request):
    """API para adicionar membros familiares."""
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            numero_paif = dados.get('numero_paif')
            membros = dados.get('membros', [])
            
            # Validar número PAIF
            try:
                ficha = FichaPAIF.objects.get(numero_paif=numero_paif)
            except FichaPAIF.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': f'Ficha PAIF {numero_paif} não encontrada'
                })
            
            # Validar e processar cada membro
            for membro in membros:
                form = MembroFamiliarForm(membro)
                if not form.is_valid():
                    return JsonResponse({
                        'success': False,
                        'message': 'Dados inválidos para um membro',
                        'errors': form.errors
                    })
            
            # Salvar os membros
            # Implementar conforme seu modelo de membros familiares
            # Exemplo: MembroFamiliar.objects.create(...)
            
            return JsonResponse({
                'success': True,
                'message': 'Membros familiares adicionados com sucesso'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.relatorios.utils.pdf_generator import gerar_pdf_instrumental

@login_required
def exportar_ficha_pdf(request, id):
    """Exporta uma ficha PAIF para formato PDF"""
    ficha = get_object_or_404(FichaPAIF, id=id)
    
    # Preparar título para o documento
    titulo = f"Ficha PAIF - {ficha.numero_paif}"
    
    # Preparar os dados da ficha para o PDF
    conteudo = {
        "nome_referencia": ficha.nome_referencia,
        "data_cadastro": ficha.data.strftime("%d/%m/%Y") if hasattr(ficha, 'data') else "",
        "cpf": ficha.cpf,
        "endereco": ficha.endereco,
        "telefone": ficha.telefone,
        "composicao_familiar": [
            {
                "nome": familiar.nome,
                "parentesco": familiar.parentesco,
                "idade": familiar.idade
            } for familiar in ficha.familiares.all()
        ],
        # Adicione outros campos conforme necessário
    }
    
    # Converter para JSON (necessário para o gerar_pdf_instrumental)
    conteudo_json = json.dumps(conteudo)
    
    # Usar a função do módulo relatórios para gerar o PDF
    return gerar_pdf_instrumental(titulo, conteudo_json)
