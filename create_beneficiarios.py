"""
###############################################################################
# Script para Criar Beneficiários a partir de Fichas PAIF
###############################################################################
#
# DESCRIÇÃO:
# Este script busca todas as Fichas PAIF que não possuem um Beneficiário 
# associado e cria os registros de Beneficiários correspondentes.
# Útil após a importação de dados do Excel quando apenas as fichas PAIF foram
# criadas corretamente, mas os beneficiários não.
#
# LÓGICA DE PROCESSAMENTO:
#   1. Procura fichas PAIF sem beneficiários associados
#   2. Cria um beneficiário para cada ficha, usando o nome do responsável
#   3. Usa valores temporários para campos obrigatórios que não estão disponíveis
#
# AUTOR: [NICK BOY]
# DATA: [Data de criação]
###############################################################################
"""

import os
import django
from datetime import datetime

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

# Importar modelos necessários depois de configurar o Django
from apps.core.models import Beneficiario, FichaPAIF
from django.db.models import OuterRef, Exists

def criar_beneficiarios():
    print("Iniciando criação de beneficiários a partir de Fichas PAIF...")
    
    # Encontrar fichas PAIF que não têm beneficiário associado
    subquery = Beneficiario.objects.filter(ficha_paif=OuterRef('pk'))
    fichas_sem_beneficiario = FichaPAIF.objects.annotate(
        tem_beneficiario=Exists(subquery)
    ).filter(tem_beneficiario=False)
    
    total_fichas = fichas_sem_beneficiario.count()
    print(f"Encontradas {total_fichas} fichas PAIF sem beneficiário associado.")
    
    criados = 0
    erros = 0
    
    # Criar beneficiários para cada ficha
    for ficha in fichas_sem_beneficiario:
        try:
            # Criar beneficiário com dados básicos da ficha
            beneficiario = Beneficiario(
                nome_completo=ficha.nome_referencia,
                data_nascimento=datetime(1900, 1, 1),  # Valor temporário
                sexo='O',  # Valor temporário (Outro)
                cpf=f"{ficha.numero_paif}00000",  # CPF temporário baseado no número PAIF
                endereco=ficha.endereco,
                nome_mae='Não informado',  # Valor temporário
                ficha_paif=ficha,
                cras=ficha.cras
            )
            
            beneficiario.save()
            criados += 1
            
            if criados % 50 == 0:
                print(f"Criados {criados} de {total_fichas} beneficiários...")
                
        except Exception as e:
            erros += 1
            print(f"Erro ao criar beneficiário para ficha {ficha.numero_paif}: {e}")
    
    print("\nProcessamento concluído!")
    print(f"Beneficiários criados: {criados}")
    print(f"Erros: {erros}")
    print(f"Total de fichas processadas: {total_fichas}")

if __name__ == '__main__':
    criar_beneficiarios()