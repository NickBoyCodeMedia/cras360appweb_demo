from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.auth_app.models import Usuario
from apps.core.models import Cidade, CRAS

class Command(BaseCommand):
    help = 'Configura grupos e permissões para o módulo de Gestão Municipal'

    def handle(self, *args, **kwargs):
        # Criar grupo de gestores
        gestores_group, created = Group.objects.get_or_create(name='gestores')
        
        # Adicionar permissões necessárias
        # Permissões para visualizar todos os modelos relevantes
        for model_name in ['cidade', 'cras', 'beneficiario', 'fichapaif', 'fichascfv', 'atividadescfv']:
            content_type = ContentType.objects.get(app_label='core', model=model_name)
            permission = Permission.objects.get(
                codename=f'view_{model_name}',
                content_type=content_type,
            )
            gestores_group.permissions.add(permission)

        # Adicionar permissão especial para acessar a gestão municipal
        try:
            content_type = ContentType.objects.get(app_label='core', model='cidade')
            gestao_perm, created = Permission.objects.get_or_create(
                codename='access_gestao_municipal',
                name='Pode acessar o módulo de gestão municipal',
                content_type=content_type,
            )
            gestores_group.permissions.add(gestao_perm)
        except ContentType.DoesNotExist:
            self.stdout.write(self.style.ERROR('Content Type para Cidade não encontrado'))

        # Criar usuário para Secretaria Municipal
        try:
            # Busca pela cidade de Breves no banco de dados
            cidade_breves = Cidade.objects.get(nome='BREVES', uf='PA')
            
            if not Usuario.objects.filter(email='semtras_breves@exemplo.com').exists():
                usuario = Usuario.objects.create_user(
                    email='semtras_breves@exemplo.com',
                    password='senha@123',
                    nome_completo='Gestor SEMTRAS Breves',
                    perfil='Coordenador',
                    is_active=True
                )
                
                # Adicionar ao grupo de gestores
                usuario.groups.add(gestores_group)
                
                self.stdout.write(self.style.SUCCESS(f'Usuário "semtras_breves" criado com sucesso'))
            else:
                usuario = Usuario.objects.get(email='semtras_breves@exemplo.com')
                # Atualizar a senha em caso de usuário existente
                usuario.set_password('senha@123')
                usuario.save()
                
                if not usuario.groups.filter(name='gestores').exists():
                    usuario.groups.add(gestores_group)
                self.stdout.write(self.style.WARNING('Usuário já existe, grupo e senha atualizados'))
                
            # Garantir que superusers tenham acesso
            for admin in Usuario.objects.filter(is_superuser=True):
                if not admin.groups.filter(name='gestores').exists():
                    admin.groups.add(gestores_group)
                    
        except Cidade.DoesNotExist:
            self.stdout.write(self.style.ERROR('Cidade de Breves não encontrada. Crie primeiro a cidade.'))