import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

from apps.auth_app.models import Usuario

def create_superuser():
    email = 'admin@cras360.com'
    password = 'demo@cras360'  # Senha padrão demo
    
    usuario = Usuario.objects.filter(email=email).first()
    
    if not usuario:
        print(f"Creating superuser: {email}")
        Usuario.objects.create_superuser(
            email=email,
            nome_completo='Administrador Demo',
            senha=password,
            perfil='Administrador'
        )
    else:
        print(f"Updating superuser password: {email}")
        usuario.set_password(password)
        usuario.save()

if __name__ == '__main__':
    create_superuser()
