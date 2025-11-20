from django import forms
from apps.core.models import FichaPAIF, Beneficiario

class FichaPAIFForm(forms.ModelForm):
    """Formulário para cadastro e edição de fichas PAIF."""
    
    class Meta:
        model = FichaPAIF
        exclude = ['data_atualizacao']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'nome_referencia': forms.TextInput(attrs={'class': 'uppercase'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'}),
            'nis': forms.TextInput(attrs={'class': 'nis-mask'}),
            'cep': forms.TextInput(attrs={'class': 'cep-mask'}),
            'telefone': forms.TextInput(attrs={'class': 'telefone-mask'}),
            'endereco': forms.TextInput(attrs={'class': 'uppercase'}),
            'bairro': forms.TextInput(attrs={'class': 'uppercase'}),
            'municipio': forms.TextInput(attrs={'class': 'uppercase'}),
            'nome_mae': forms.TextInput(attrs={'class': 'uppercase'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.Textarea):
                field.widget.attrs['placeholder'] = field.label

class PesquisaPAIFForm(forms.Form):
    """Formulário para pesquisa de fichas PAIF."""
    numero_paif = forms.CharField(required=False, label="Número PAIF")
    nome = forms.CharField(required=False, label="Nome da Referência Familiar")
    cpf = forms.CharField(required=False, label="CPF")
    bairro = forms.CharField(required=False, label="Bairro")
    data_inicial = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Data Inicial")
    data_final = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Data Final")
    cras = forms.IntegerField(required=False, widget=forms.HiddenInput())

class EvolucaoAtendimentoForm(forms.Form):
    """Formulário para evolução de atendimento PAIF."""
    data_atendimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    descricao = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label="Descrição do Atendimento")
    tecnico = forms.CharField(widget=forms.HiddenInput())
    cras = forms.CharField(widget=forms.HiddenInput())
    numero_paif = forms.CharField(widget=forms.HiddenInput())

class MembroFamiliarForm(forms.Form):
    """Formulário para adicionar ou editar membros da família."""
    nome = forms.CharField(max_length=100)
    parentesco = forms.CharField(max_length=50)
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    frequencia_escolar = forms.ChoiceField(choices=[('Sim', 'Sim'), ('Não', 'Não')])
    escola = forms.CharField(max_length=100, required=False)
    serie = forms.CharField(max_length=50, required=False)
    turno = forms.ChoiceField(choices=[('MANHÃ', 'MANHÃ'), ('TARDE', 'TARDE'), ('NOITE', 'NOITE')], required=False)
    situacao_trabalho = forms.ChoiceField(choices=[
        ('ESTUDANTE', 'ESTUDANTE'),
        ('EMPREGADO', 'EMPREGADO'),
        ('DESEMPREGADO', 'DESEMPREGADO'),
        ('AUTÔNOMO', 'AUTÔNOMO'),
    ])
    renda = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
