from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'nome_completo', 'perfil', 'cras', 'is_active', 'is_staff')
    search_fields = ('email', 'nome_completo')
    list_filter = ('perfil', 'cras', 'is_active', 'is_staff')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'perfil', 'cras')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'perfil', 'cras', 'password1', 'password2'),
        }),
    )
    
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    autocomplete_fields = ['cras']


admin.site.register(Usuario, UsuarioAdmin)
