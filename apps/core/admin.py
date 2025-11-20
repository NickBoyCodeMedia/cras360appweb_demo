from django.contrib import admin
from .models import Cidade, CRAS, Beneficiario, FichaPAIF, FichaSCFV, AtividadeSCFV, Agendamento

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uf', 'populacao')
    search_fields = ('nome', 'uf')
    list_filter = ('uf',)
    ordering = ('uf', 'nome')

@admin.register(CRAS)
class CRASAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'endereco', 'telefone', 'coordenador')
    search_fields = ('nome', 'cidade__nome', 'endereco')
    list_filter = ('cidade__uf', 'cidade')
    autocomplete_fields = ['cidade']

@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'data_nascimento', 'cras')
    search_fields = ('nome_completo', 'cpf', 'nis', 'rg')
    list_filter = ('cras', 'sexo')
    autocomplete_fields = ['cras', 'ficha_paif']
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'sexo', 'cpf', 'rg', 'nis')
        }),
        ('Filiação', {
            'fields': ('nome_mae', 'nome_pai')
        }),
        ('Endereço', {
            'fields': ('endereco',)
        }),
        ('Vinculação', {
            'fields': ('cras', 'ficha_paif')
        }),
    )

@admin.register(FichaPAIF)
class FichaPAIFAdmin(admin.ModelAdmin):
    list_display = ('numero_paif', 'nome_referencia', 'data', 'cras')
    search_fields = ('numero_paif', 'nome_referencia', 'cpf')
    list_filter = ('cras', 'data')
    date_hierarchy = 'data'
    autocomplete_fields = ['cras']

# Registre os outros modelos conforme necessário
admin.site.register(FichaSCFV)
admin.site.register(AtividadeSCFV)
admin.site.register(Agendamento)
