from django.core.management.base import BaseCommand
from apps.auth_app.models import Usuario

class Command(BaseCommand):
    help = 'Cria um usuário administrador para o sistema CRAS360'

    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Criando usuário administrador...'))
            Usuario.objects.create_superuser(
                email='admin@cras360.com',
                nome_completo='Administrador do Sistema',
                senha='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Usuário administrador criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('Já existe pelo menos um superusuário cadastrado.'))
