from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Função helper para verificar permissões
def verificar_permissao_relatorio(request, tipo_relatorio):
    """
    Verifica se o usuário tem permissão para acessar o tipo de relatório.
    
    Args:
        tipo_relatorio: 'scfv', 'paif' ou None (para página inicial)
        
    Returns:
        Boolean indicando se o usuário tem permissão
    """
    # Se o usuário é superuser, tem permissão total
    if request.user.is_superuser:
        return True
        
    # Obtenha o perfil do usuário (várias tentativas para diferentes estruturas)
    perfil_usuario = None
    
    # Método 1: Através do relacionamento OneToOne
    try:
        perfil_usuario = request.user.perfilusuario.perfil
        print(f"Perfil obtido pelo método 1: {perfil_usuario}")
    except Exception as e:
        print(f"Erro ao obter perfil pelo método 1: {e}")
        pass
        
    # Método 2: Atributo direto no usuário
    if not perfil_usuario:
        try:
            perfil_usuario = getattr(request.user, 'perfil', None)
            print(f"Perfil obtido pelo método 2: {perfil_usuario}")
        except Exception as e:
            print(f"Erro ao obter perfil pelo método 2: {e}")
            pass
    
    # Método 3: Via sessão
    if not perfil_usuario:
        perfil_usuario = request.session.get('user_perfil', None)
        print(f"Perfil obtido pelo método 3: {perfil_usuario}")
    
    # Método 4: Via atributo HTML
    if not perfil_usuario and hasattr(request, 'META'):
        # Tente obter do HTTP_USER_AGENT ou outras informações de cabeçalho
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'data-user-perfil=' in user_agent:
            import re
            match = re.search(r'data-user-perfil=["\'](.*?)["\']', user_agent)
            if match:
                perfil_usuario = match.group(1)
                print(f"Perfil obtido pelo método 4: {perfil_usuario}")
    
    # Se ainda não temos perfil, retornar falso
    if not perfil_usuario:
        print("Não foi possível determinar o perfil do usuário")
        
        # Para fins de depuração, verificamos se estamos em um ambiente de desenvolvimento
        if 'localhost' in request.META.get('HTTP_HOST', '') or '127.0.0.1' in request.META.get('HTTP_HOST', ''):
            # Em desenvolvimento, verificamos se há algum identificador no user agent que indique ser um técnico
            user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
            if 'técnico' in user_agent or 'tecnico' in user_agent:
                print("Perfil técnico detectado pelo User-Agent")
                perfil_usuario = 'Técnico'
            elif hasattr(request.user, 'username') and request.user.username:
                # Se for um usuário com nome, consideramos como técnico para teste
                if 'tec' in request.user.username.lower():
                    print(f"Perfil técnico assumido pelo username: {request.user.username}")
                    perfil_usuario = 'Técnico'
        
        if not perfil_usuario:
            return False
    
    print(f"Perfil final utilizado: {perfil_usuario}")
    
    # Normaliza o perfil para comparação (remove acentos e converte para minúsculo)
    perfil_normalizado = perfil_usuario.lower().replace(' ', '_').replace('-', '_')
    
    # Remover acentos para padronização
    try:
        import unicodedata
        perfil_normalizado = unicodedata.normalize('NFKD', perfil_normalizado)\
            .encode('ASCII', 'ignore').decode('ASCII')
    except Exception as e:
        print(f"Erro ao normalizar perfil: {e}")
    
    print(f"Perfil normalizado: {perfil_normalizado}")
    
    # Coordenador e desenvolvedor têm acesso a todos os relatórios
    if perfil_normalizado in ['coordenador', 'desenvolvedor', 'administrador']:
        print(f"Acesso permitido para {perfil_usuario} (todos relatórios)")
        return True
    
    # Assistentes sociais só podem acessar relatórios PAIF
    if perfil_normalizado in ['assistente_social', 'assistente']:
        tem_acesso = tipo_relatorio == 'paif' or tipo_relatorio is None
        print(f"Assistente Social acessando {tipo_relatorio}: {tem_acesso}")
        return tem_acesso
    
    # AQUI ESTÁ A CORREÇÃO: Verificação melhorada para perfis técnicos
    # Verificação específica para os vários formatos possíveis de "Técnico"
    if perfil_normalizado == 'tecnico' or 'tecnic' in perfil_normalizado or 'tecnico_pedagogico' in perfil_normalizado:
        tem_acesso = tipo_relatorio == 'scfv' or tipo_relatorio is None
        print(f"Técnico acessando {tipo_relatorio}: {tem_acesso}")
        return tem_acesso
        
    # Regra simples: Se o perfil começar com "tec", consideramos como técnico
    if perfil_normalizado.startswith('tec'):
        tem_acesso = tipo_relatorio == 'scfv' or tipo_relatorio is None
        print(f"Perfil que começa com 'tec' ({perfil_usuario}) acessando {tipo_relatorio}: {tem_acesso}")
        return tem_acesso
    
    # Para outros perfis, pode-se definir regras adicionais aqui
    # Por padrão, negamos o acesso
    print(f"Perfil não reconhecido: {perfil_usuario} - Acesso negado para {tipo_relatorio}")
    return False

# Função principal para a página inicial de relatórios
@login_required
def index(request):
    """Página principal do módulo de relatórios"""
    # Verificar se o usuário tem acesso à página de relatórios
    if not verificar_permissao_relatorio(request, None):
        messages.error(request, "Você não tem permissão para acessar o módulo de relatórios.")
        return redirect('index')
        
    # Determinar quais relatórios o usuário pode acessar
    pode_acessar_scfv = verificar_permissao_relatorio(request, 'scfv')
    pode_acessar_paif = verificar_permissao_relatorio(request, 'paif')
    
    context = {
        'pode_acessar_scfv': pode_acessar_scfv,
        'pode_acessar_paif': pode_acessar_paif
    }
    return render(request, 'relatorios/relatorios.html', context)

# Páginas específicas de relatórios
@login_required
def scfv_index(request):
    """Página de relatórios SCFV"""
    if not verificar_permissao_relatorio(request, 'scfv'):
        messages.error(request, "Você não tem permissão para acessar relatórios SCFV.")
        return redirect('relatorios:index')
        
    context = {'cras_list': []}  # Lista vazia para início
    return render(request, 'relatorios/scfv_report.html', context)

@login_required
def paif_index(request):
    """Página de relatórios PAIF"""
    if not verificar_permissao_relatorio(request, 'paif'):
        messages.error(request, "Você não tem permissão para acessar relatórios PAIF.")
        return redirect('relatorios:index')
        
    context = {'cras_list': []}  # Lista vazia para início
    return render(request, 'relatorios/paif_report.html', context)

# APIs para relatórios
@login_required
def api_scfv(request):
    """API para obter dados dos relatórios SCFV"""
    if not verificar_permissao_relatorio(request, 'scfv'):
        return JsonResponse({
            'success': False,
            'message': 'Sem permissão para acessar relatórios SCFV'
        }, status=403)
        
    data = {
        'success': True,
        'headers': ['Nome', 'Projeto', 'Idade', 'Data Cadastro'],
        'rows': [
            ['João Silva', 'SOMOS TÃO JOVENS', '12', '01/01/2023']
        ]
    }
    return JsonResponse(data)

@login_required
def api_paif(request):
    """API para obter dados dos relatórios PAIF"""
    if not verificar_permissao_relatorio(request, 'paif'):
        return JsonResponse({
            'success': False,
            'message': 'Sem permissão para acessar relatórios PAIF'
        }, status=403)
        
    data = {
        'success': True,
        'headers': ['Nº PAIF', 'Nome Referência', 'CPF', 'Data Cadastro'],
        'rows': [
            ['001', 'Ana Souza', '123.456.789-00', '01/01/2023']
        ]
    }
    return JsonResponse(data)

# Exportação de relatórios
@login_required
def exportar_relatorio(request, tipo, formato):
    """Exportar relatórios em diferentes formatos"""
    if not verificar_permissao_relatorio(request, tipo):
        messages.error(request, f"Você não tem permissão para exportar relatórios {tipo.upper()}.")
        return redirect('relatorios:index')
        
    return HttpResponse(f"Exportando relatório {tipo} em formato {formato}")

# Visualização de fichas
@login_required
def scfv_ficha_cadastro(request, id):
    """Visualização de ficha de cadastro SCFV"""
    if not verificar_permissao_relatorio(request, 'scfv'):
        messages.error(request, "Você não tem permissão para acessar fichas SCFV.")
        return redirect('relatorios:index')
        
    context = {'ficha': {'id': id, 'nome': 'Nome do Beneficiário', 'tipo': 'SCFV'}}
    return render(request, 'relatorios/scfv_ficha.html', context)

@login_required
def paif_ficha_cadastro(request, id):
    """Visualização de ficha de cadastro PAIF"""
    if not verificar_permissao_relatorio(request, 'paif'):
        messages.error(request, "Você não tem permissão para acessar fichas PAIF.")
        return redirect('relatorios:index')
        
    context = {'ficha': {'id': id, 'nome': 'Nome do Beneficiário', 'tipo': 'PAIF'}}
    return render(request, 'relatorios/paif_ficha.html', context)

# Geração de relatórios
@login_required
def gerar_scfv(request):
    """Gerar relatório SCFV com base nos filtros"""
    if not verificar_permissao_relatorio(request, 'scfv'):
        messages.error(request, "Você não tem permissão para gerar relatórios SCFV.")
        return redirect('relatorios:index')
        
    return render(request, 'relatorios/scfv_report.html')

@login_required
def gerar_paif(request):
    """Gerar relatório PAIF com base nos filtros"""
    if not verificar_permissao_relatorio(request, 'paif'):
        messages.error(request, "Você não tem permissão para gerar relatórios PAIF.")
        return redirect('relatorios:index')
        
    return render(request, 'relatorios/paif_report.html')

# Verificação de permissões
@login_required
def verificar_permissao_ajax(request, tipo_relatorio):
    """API para verificar permissões de acesso aos relatórios via AJAX"""
    tem_permissao = verificar_permissao_relatorio(request, tipo_relatorio)
    
    return JsonResponse({
        'tem_permissao': tem_permissao,
        'tipo_relatorio': tipo_relatorio
    })

# Função para depuração de permissões
@login_required
def debug_permissoes(request):
    """
    View para diagnóstico de problemas de permissão.
    Exibe detalhadamente as informações do usuário e suas permissões.
    """
    # Coletando informações sobre o usuário
    user_info = {
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
        'is_authenticated': request.user.is_authenticated
    }
    
    # Tentando obter todas as propriedades possíveis do perfil
    perfil_info = {}
    
    # Método 1: Direto do relacionamento OneToOne
    try:
        perfil = request.user.perfilusuario
        perfil_info['perfilusuario'] = {
            'perfil': getattr(perfil, 'perfil', None),
            'ativo': getattr(perfil, 'ativo', None),
            'data_cadastro': getattr(perfil, 'data_cadastro', None),
        }
        if hasattr(perfil, 'cras'):
            perfil_info['perfilusuario']['cras'] = str(perfil.cras)
    except Exception as e:
        perfil_info['perfilusuario_error'] = str(e)
    
    # Método 2: Atributos diretos no usuário
    attributes = ['perfil', 'tipo_usuario', 'role', 'grupo']
    for attr in attributes:
        try:
            value = getattr(request.user, attr, None)
            if value:
                perfil_info[f'user_{attr}'] = str(value)
        except Exception as e:
            perfil_info[f'user_{attr}_error'] = str(e)
    
    # Método 3: Informações da sessão
    session_info = {}
    for key in request.session.keys():
        if 'perfil' in key.lower() or 'user' in key.lower() or 'permis' in key.lower():
            session_info[key] = request.session[key]
    
    # Método 4: Informações do META
    meta_info = {}
    for key, value in request.META.items():
        if isinstance(value, str) and ('user' in key.lower() or 'auth' in key.lower()):
            meta_info[key] = value
    
    # Testando permissões específicas
    permissoes = {
        'pagina_inicial': verificar_permissao_relatorio(request, None),
        'relatorios_scfv': verificar_permissao_relatorio(request, 'scfv'),
        'relatorios_paif': verificar_permissao_relatorio(request, 'paif')
    }
    
    # Renderizar página de diagnóstico
    context = {
        'user_info': user_info,
        'perfil_info': perfil_info,
        'session_info': session_info,
        'meta_info': meta_info,
        'permissoes': permissoes
    }
    
    return render(request, 'relatorios/debug_permissoes.html', context)
