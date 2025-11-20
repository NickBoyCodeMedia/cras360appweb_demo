import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

from apps.auth_app.models import Usuario

def criar_usuarios_padrao():
    # Senha padrão para todos
    SENHA_PADRAO = 'demo@cras360'
    
    # Lista de usuários a criar (Apenas Recepção e Técnico Pedagogo)
    usuarios = [
        {
            'email': 'recepcao@cras360.com',
            'nome_completo': 'Maria Recepção (Demo)',
            'senha': SENHA_PADRAO,
            'perfil': 'Recepção',
        },
        {
            'email': 'tecnico@cras360.com',
            'nome_completo': 'Silvia Pedagoga (Demo)',
            'senha': SENHA_PADRAO,
            'perfil': 'Técnico',
        }
    ]

    print(f"Iniciando criação de usuários DEMO com senha padrão: {SENHA_PADRAO}")

    # Criar usuários se não existirem
    for usuario_data in usuarios:
        email = usuario_data['email']
        
        # Verificar se usuário já existe
        usuario = Usuario.objects.filter(email=email).first()
        
        if not usuario:
            print(f"Criando usuário: {email} - {usuario_data['nome_completo']} ({usuario_data['perfil']})")
            Usuario.objects.create_user(
                email=email,
                nome_completo=usuario_data['nome_completo'],
                senha=usuario_data['senha'],
                perfil=usuario_data['perfil'],
                is_active=True
            )
        else:
            print(f"Atualizando senha do usuário existente: {email}")
            usuario.set_password(usuario_data['senha'])
            usuario.save()

    print("\nUsuários DEMO configurados com sucesso!")
    print("\n| Email                 | Senha         | Perfil                |")
    print("|----------------------|---------------|------------------------|")
    for usuario_data in usuarios:
        email_padded = usuario_data['email'].ljust(22)
        senha_padded = usuario_data['senha'].ljust(15)
        print(f"| {email_padded}| {senha_padded}| {usuario_data['perfil']}")

if __name__ == '__main__':
    criar_usuarios_padrao()
