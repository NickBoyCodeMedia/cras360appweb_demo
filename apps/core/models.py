from django.db import models
from django.conf import settings
from datetime import datetime

class Cidade(models.Model):
    """Modelo para representar cidades."""
    nome = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    populacao = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome}/{self.uf}"

class CRAS(models.Model):
    """Modelo para representar unidades do CRAS."""
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    coordenador = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "CRAS"
        verbose_name_plural = "CRAS"

class PerfilUsuario(models.Model):
    """Perfil estendido para o modelo de usuário do Django."""
    PERFIS = (
        ('desenvolvedor', 'Desenvolvedor'),
        ('coordenador', 'Coordenador'),
        ('assistente_social', 'Assistente Social'),
        ('tecnico_pedagogico', 'Técnico Pedagógico'),
        ('orientador', 'Orientador'),
        ('recepcionista', 'Recepcionista'),
    )
    
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=50, choices=PERFIS)
    data_cadastro = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    cras = models.ForeignKey(CRAS, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_perfil_display()}"

class FichaPAIF(models.Model):
    """Modelo para ficha PAIF (Proteção e Atendimento Integral à Família)."""
    numero_paif = models.CharField(max_length=50, unique=True, help_text="Número único da família no PAIF")
    tipo = models.CharField(max_length=20, choices=[('inclusao', 'Inclusão'), ('atualizacao', 'Atualização')], default='inclusao')
    data = models.DateField()
    nome_referencia = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20, blank=True, null=True)
    nis = models.CharField(max_length=20, blank=True, null=True)
    nome_mae = models.CharField(max_length=100, blank=True, null=True)
    raca = models.CharField(max_length=20, choices=[
        ('branca', 'Branca'),
        ('parda', 'Parda'),
        ('negra', 'Negra'),
        ('quilombola', 'Quilombola'),
        ('indigena', 'Indígena'),
        ('outra', 'Outra')
    ], blank=True, null=True)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    municipio = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    
    # Características do domicílio
    moradia = models.CharField(max_length=20, choices=[
        ('propria', 'Própria'),
        ('alugada', 'Alugada'),
        ('financiada', 'Financiada'),
        ('cedida', 'Cedida'),
        ('ocupacao', 'Ocupação'),
        ('outra', 'Outra')
    ], null=True, blank=True)
    moradia_outra = models.CharField(max_length=50, blank=True, null=True)
    num_comodos = models.IntegerField(null=True, blank=True)
    num_quartos = models.IntegerField(null=True, blank=True)
    
    # Tipo de construção
    tipo_construcao = models.CharField(max_length=30, choices=[
        ('tijolo', 'Tijolo/Alvenaria'),
        ('taipa_revestida', 'Taipa Revestida'),
        ('taipa_nao_revestida', 'Taipa Não Revestida'),
        ('madeira', 'Madeira'),
        ('madeira_reaproveitada', 'Madeira Reaproveitada'),
        ('outros', 'Outros')
    ], null=True, blank=True)
    tipo_construcao_outros = models.CharField(max_length=50, blank=True, null=True)
    
    # Local de risco
    local_risco = models.CharField(max_length=3, choices=[('sim', 'Sim'), ('nao', 'Não')], default='nao', null=True, blank=True)
    
    # Energia elétrica
    energia_eletrica = models.CharField(max_length=20, choices=[
        ('relogio', 'Relógio'),
        ('improvisado', 'Improvisado'),
        ('outros', 'Outros')
    ], null=True, blank=True)
    energia_eletrica_outros = models.CharField(max_length=50, blank=True, null=True)
    
    # Instalação sanitária
    instalacao_sanitaria = models.CharField(max_length=20, choices=[
        ('fossa_septica', 'Fossa Séptica'),
        ('fossa_rudimentar', 'Fossa Rudimentar')
    ], null=True, blank=True)
    
    # Destino do esgoto
    destino_esgoto = models.CharField(max_length=20, choices=[
        ('ceu_aberto', 'Céu Aberto'),
        ('fossa', 'Fossa'),
        ('outro', 'Outro')
    ], null=True, blank=True)
    
    # Abastecimento de água
    abastecimento_agua = models.CharField(max_length=30, choices=[
        ('rede_publica', 'Rede Pública Encanada'),
        ('carro_pipa', 'Carro Pipa / Poço'),
        ('correntes_naturais', 'Correntes de Água Natural'),
        ('torneira_coletiva', 'Torneiras Coletivas'),
        ('outro', 'Outro')
    ], null=True, blank=True)
    
    # Destino do lixo
    destino_lixo = models.CharField(max_length=30, choices=[
        ('coleta_domiciliar', 'Coleta Domiciliar'),
        ('queimado', 'Queimado'),
        ('cacamba', 'Caçamba'),
        ('enterrado', 'Enterrado'),
        ('outro', 'Outro')
    ], null=True, blank=True)
    
    # Receita mensal e benefícios
    num_integrantes = models.IntegerField(null=True, blank=True)
    num_trabalham = models.IntegerField(null=True, blank=True)
    renda_total = models.CharField(max_length=20, blank=True, null=True)
    beneficios = models.CharField(max_length=50, blank=True, null=True)
    
    # Despesas mensais
    despesa_aluguel = models.CharField(max_length=20, blank=True, null=True)
    despesa_alimentacao = models.CharField(max_length=20, blank=True, null=True)
    despesa_agua = models.CharField(max_length=20, blank=True, null=True)
    despesa_luz = models.CharField(max_length=20, blank=True, null=True)
    despesa_transporte = models.CharField(max_length=20, blank=True, null=True)
    despesa_gas = models.CharField(max_length=20, blank=True, null=True)
    
    # Campos de demanda (usando BooleanField para checkboxes)
    demanda_espontane = models.BooleanField(default=False)
    demanda_encaminada = models.BooleanField(default=False)
    demanda_buscativa = models.BooleanField(default=False)
    demanda_outros = models.BooleanField(default=False)
    
    # Campos administrativos
    cras = models.ForeignKey(CRAS, on_delete=models.PROTECT)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_paif:
            # Gerar número PAIF baseado em ano + sequencial
            ano_atual = datetime.now().year
            ultimo = FichaPAIF.objects.filter(
                numero_paif__startswith=f"{ano_atual}-"
            ).order_by('-numero_paif').first()
            
            if ultimo:
                ultimo_seq = int(ultimo.numero_paif.split('-')[1])
                prox_seq = ultimo_seq + 1
            else:
                prox_seq = 1
                
            self.numero_paif = f"{ano_atual}-{prox_seq:04d}"  # Ex: 2025-0001
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"PAIF {self.numero_paif} - {self.nome_referencia}"
    
    class Meta:
        verbose_name = "Ficha PAIF"
        verbose_name_plural = "Fichas PAIF"

class Beneficiario(models.Model):
    """Modelo para representar beneficiários do CRAS."""
    nome_completo = models.CharField(max_length=200)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=1)
    cpf = models.CharField(max_length=14) # cpf = models.CharField(max_length=14, unique=True)
    nis = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    nome_mae = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100, blank=True, null=True)
    ficha_paif = models.ForeignKey(FichaPAIF, on_delete=models.SET_NULL, null=True, blank=True)
    cras = models.ForeignKey(CRAS, on_delete=models.PROTECT, null=True)
    
    @property
    def numero_paif(self):
        """Retorna o número PAIF da família do beneficiário, se disponível."""
        if self.ficha_paif:
            return self.ficha_paif.numero_paif
        return None
    
    def __str__(self):
        if self.ficha_paif:
            return f"{self.nome_completo} (PAIF: {self.ficha_paif.numero_paif})"
        return self.nome_completo

class FichaSCFV(models.Model):
    """Modelo para ficha SCFV (Serviço de Convivência e Fortalecimento de Vínculos)."""
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    data_entrada = models.DateField()
    situacao_escolar = models.CharField(max_length=100)
    publico_prioritario = models.CharField(max_length=255)
    beneficio_social = models.CharField(max_length=100, blank=True, null=True)
    pressao_alta = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    outros_saude = models.CharField(max_length=255, blank=True)
    observacoes = models.TextField(blank=True)
    
    def __str__(self):
        return f"SCFV - {self.beneficiario.nome_completo}"
    
    class Meta:
        verbose_name = "Ficha SCFV"
        verbose_name_plural = "Fichas SCFV"

class AtividadeSCFV(models.Model):
    """Modelo para atividades do SCFV."""
    nome_atividade = models.CharField(max_length=100)
    descricao = models.TextField()
    faixa_etaria = models.CharField(max_length=50)
    frequencia_esperada = models.CharField(max_length=50)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    cras = models.ForeignKey(CRAS, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome_atividade

class ParticipacaoSCFV(models.Model):
    """Modelo para registrar participação nas atividades SCFV."""
    ficha_scfv = models.ForeignKey(FichaSCFV, on_delete=models.CASCADE)
    atividade = models.ForeignKey(AtividadeSCFV, on_delete=models.CASCADE)
    data_participacao = models.DateField()
    observacoes = models.TextField(blank=True)
    avaliacao = models.TextField(blank=True)
    
    def __str__(self):
        return f"Participação: {self.ficha_scfv.beneficiario.nome_completo} - {self.atividade.nome_atividade}"

class Agendamento(models.Model):
    """Modelo para agendamentos de atendimento."""
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agendamentos_tecnicos')
    data = models.DateField()
    hora = models.TimeField()
    tipo_atendimento = models.CharField(max_length=50)
    observacao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('agendado', 'Agendado'),
            ('compareceu', 'Compareceu'),
            ('nao_compareceu', 'Não Compareceu'),
            ('cancelado', 'Cancelado')
        ],
        default='agendado'
    )
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='agendamentos_criados')
    data_criacao = models.DateTimeField(auto_now_add=True)

class DemandaEspontanea(models.Model):
    """Modelo para registro de demandas espontâneas."""
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    tipo_atendimento = models.CharField(max_length=50)
    motivo_procura = models.TextField()
    prioridade = models.CharField(
        max_length=20, 
        choices=[
            ('normal', 'Normal'),
            ('alta', 'Alta'),
            ('urgente', 'Urgente')
        ],
        default='normal'
    )
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_registro = models.DateTimeField()
    
class Atendimento(models.Model):
    """Modelo para atendimentos realizados."""
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='atendimentos')
    tipo_atendimento = models.CharField(max_length=50)
    origem = models.CharField(
        max_length=20, 
        choices=[
            ('agendamento', 'Agendamento'),
            ('demanda_espontanea', 'Demanda Espontânea'),
            ('encaminhamento', 'Encaminhamento')
        ]
    )
    agendamento = models.ForeignKey(Agendamento, on_delete=models.SET_NULL, null=True, blank=True)
    demanda_relacionada = models.ForeignKey(DemandaEspontanea, on_delete=models.SET_NULL, null=True, blank=True)
    data_atendimento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('aguardando', 'Aguardando'),
            ('em_andamento', 'Em Andamento'),
            ('finalizado', 'Finalizado'),
            ('cancelado', 'Cancelado')
        ],
        default='aguardando'
    )
    resumo = models.TextField(null=True, blank=True)
    evolucao = models.TextField(null=True, blank=True)