# apps/relatorios/permissions.py
from django.contrib.auth.mixins import UserPassesTestMixin

class RelatorioPermissionMixin(UserPassesTestMixin):
    """Base mixin para controle de acesso aos relatórios"""
    
    def test_func(self):
        perfil = self.request.user.perfil
        report_type = self.kwargs.get('report_type')
        
        # Acesso total para admin e coordenador
        if perfil in ['admin', 'coordenador']:
            return True
            
        # Mapeamento de perfis para tipos de relatórios permitidos
        permissoes = {
            'assistente_social': ['atendimentos', 'familias'],
            'tecnico_paif': ['paif', 'familias'],
            'tecnico_scfv': ['scfv', 'frequencia'],
            # outros perfis...
        }
        
        return perfil in permissoes and report_type in permissoes[perfil]