from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def debug_auth(request):
    """View para depurar problemas de autenticação."""
    Usuario = get_user_model()
    
    # Obter informações sobre todos os usuários
    users = Usuario.objects.all()
    users_info = []
    for user in users:
        user_info = {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'perfil': getattr(user, 'perfil', 'N/A'),
            'last_login': user.last_login,
            'groups': [g.name for g in user.groups.all()]
        }
        users_info.append(user_info)
    
    # Obter informações sobre grupos
    groups = Group.objects.all()
    groups_info = []
    for group in groups:
        group_info = {
            'name': group.name,
            'users_count': group.user_set.count(),
            'permissions_count': group.permissions.count(),
        }
        groups_info.append(group_info)
        
    # Buscar especificamente o usuário gestor
    gestor = Usuario.objects.filter(email='semtras_breves@exemplo.com').first()
    gestor_info = None
    
    if gestor:
        gestor_info = {
            'id': gestor.id,
            'email': gestor.email,
            'is_active': gestor.is_active,
            'password_hash': str(gestor.password),
            'perfil': getattr(gestor, 'perfil', 'N/A'),
            'groups': [g.name for g in gestor.groups.all()],
            'last_login': gestor.last_login,
        }
    
    context = {
        'users_count': users.count(),
        'users_info': users_info,
        'groups_info': groups_info,
        'gestor_info': gestor_info,
    }
    
    return render(request, 'auth_app/debug_auth.html', context)
