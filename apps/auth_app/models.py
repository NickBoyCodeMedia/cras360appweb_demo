from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.core.models import CRAS


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome_completo, senha=None, **extra_fields):
        if not email:
            raise ValueError('O campo de email é obrigatório')
        
        email = self.normalize_email(email)
        user = self.model(email=email, nome_completo=nome_completo, **extra_fields)
        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome_completo, senha=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('perfil', 'Desenvolvedor')
        
        return self.create_user(email, nome_completo, senha, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    PERFIL_CHOICES = (
        ('Recepção', 'Recepção'),
        ('Assistente Social', 'Assistente Social'),
        ('Técnico PAIF', 'Técnico PAIF'),
        ('Técnico SCFV', 'Técnico SCFV'),
        ('Técnico', 'Técnico'),
        ('Auxiliar Administrativo', 'Auxiliar Administrativo'),
        ('Coordenador', 'Coordenador'),
        ('Desenvolvedor', 'Desenvolvedor'),
    )
    
    email = models.EmailField(unique=True)
    nome_completo = models.CharField(max_length=150)
    perfil = models.CharField(max_length=30, choices=PERFIL_CHOICES, default='Técnico')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cras = models.ForeignKey(CRAS, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Unidade CRAS")
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo']
    
    def __str__(self):
        return self.nome_completo
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
