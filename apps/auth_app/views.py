from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
import logging

# Configurar logger para diagnóstico
logger = logging.getLogger('auth_app')

def login_view(request):
    """View para login de usuários."""
    if request.method == 'POST':
        email = request.POST.get('username')  # Campo pode ser 'username' no formulário
        senha = request.POST.get('password')  # Campo pode ser 'password' no formulário
        
        if not email:
            email = request.POST.get('email')  # Tenta com nome alternativo
            
        if not senha:
            senha = request.POST.get('senha')  # Tenta com nome alternativo
        
        logger.debug(f"Tentativa de login para o email: {email}")
        logger.debug(f"Campos do POST: {list(request.POST.keys())}")
        
        # Log mais detalhado para debug
        from apps.auth_app.models import Usuario
        user_exists = Usuario.objects.filter(email=email).exists()
        logger.debug(f"Usuário existe no banco? {user_exists}")
        
        if user_exists:
            usuario = Usuario.objects.get(email=email)
            logger.debug(f"Detalhes do usuário encontrado - ID: {usuario.id}, Perfil: {usuario.perfil}, Ativo: {usuario.is_active}")
            logger.debug(f"Hash da senha armazenada: {usuario.password[:20]}...")
        
        # Tentativa de autenticação
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            logger.info(f"Usuário autenticado com sucesso: {email}")
            logger.debug(f"Detalhes do usuário autenticado: is_active={user.is_active}, perfil={getattr(user, 'perfil', 'N/A')}")
            
            if user.is_active:
                login(request, user)
                logger.info(f"Login realizado com sucesso para {email}")
                
                # Verificar se há next na URL
                next_url = request.GET.get('next')
                if next_url:
                    logger.debug(f"Redirecionando para: {next_url}")
                    return redirect(next_url)
                else:
                    logger.debug("Redirecionando para dashboard")
                    return redirect('dashboard')
            else:
                logger.warning(f"Tentativa de login com conta inativa: {email}")
                messages.error(request, 'Conta inativa. Entre em contato com o administrador.')
        else:
            # Debug detalhado
            logger.warning(f"Falha na autenticação para {email}")
            try:
                # Tentando autenticar de novo com backend explícito
                from django.contrib.auth import get_backends
                backends = get_backends()
                logger.debug(f"Backends de autenticação disponíveis: {[b.__class__.__name__ for b in backends]}")
                
                for backend in backends:
                    auth_user = backend.authenticate(request, username=email, password=senha)
                    logger.debug(f"Tentativa com backend {backend.__class__.__name__}: {'Sucesso' if auth_user else 'Falha'}")
                
                messages.error(request, 'Email ou senha incorretos. Por favor, tente novamente.')
            except Exception as e:
                logger.exception(f"Erro ao verificar autenticação: {str(e)}")
                messages.error(request, 'Ocorreu um erro durante a autenticação.')
    
    # Renderiza o formulário de login
    form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    """View para logout de usuários."""
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')
