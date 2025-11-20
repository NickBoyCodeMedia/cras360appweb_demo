"""
###############################################################################
# Script de Importação de Dados PAIF para CRAS360
###############################################################################
#
# DESCRIÇÃO:
# Este script importa dados de famílias do PAIF (Serviço de Proteção e 
# Atendimento Integral à Família) a partir de um arquivo Excel para o sistema
# CRAS360. O script é capaz de:
#   1. Criar novos registros de FichaPAIF e Beneficiários
#   2. Atualizar registros existentes quando encontrar números PAIF duplicados
#   3. Tratar valores ausentes, inválidos ou inconsistentes
#
# ARQUIVOS EXCEL SUPORTADOS:
# O arquivo Excel deve conter as seguintes colunas:
#   - numero_paif: Identificador único da ficha PAIF
#   - data: Data de cadastro no formato DD/MM/AAAA ou AAAA-MM-DD
#   - responsavel_familiar: Nome completo da pessoa responsável
#   - endereco: Endereço da família (pode estar vazio)
#   - numero: Número do endereço (pode estar vazio)
#   - bairro: Bairro (pode estar vazio)
#   - num_integrantes: Quantidade de pessoas na família (aceita números ou 'Não informado')
#   - cras_id: ID do CRAS responsável (deve existir no banco de dados)
#   - municipio: Nome do município (pode estar vazio)
#
# LÓGICA DE PROCESSAMENTO:
#   1. Se um número PAIF já existir no banco de dados:
#      - Verifica campos vazios no registro existente
#      - Atualiza com dados do Excel se forem mais completos
#      - Mantém o registro original se os dados forem iguais ou mais completos
#
#   2. Se um número PAIF não existir:
#      - Cria um novo registro FichaPAIF
#      - Cria um novo registro Beneficiário vinculado à ficha
#
#   3. Tratamento especial:
#      - Endereços vazios: substitui por "Endereço não informado"
#      - Valores não numéricos em num_integrantes: substitui por valor padrão 1
#      - Campos obrigatórios ausentes: usa valores temporários que devem ser 
#        atualizados posteriormente (sinalizados na saída do script)
#
# REQUISITOS:
#   - Django configurado com os modelos FichaPAIF, Beneficiario, CRAS, Cidade
#   - pandas para leitura do Excel
#
# AUTOR: [NICKBOY]
# DATA: [Data de criação/última atualização]
###############################################################################
"""

import os
import pandas as pd
import django
from datetime import datetime

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

# Importar modelos necessários depois de configurar o Django
from apps.core.models import Beneficiario, FichaPAIF, CRAS, Cidade

def importar_dados_excel(caminho_arquivo):
    print(f"Iniciando importação de dados do arquivo: {caminho_arquivo}")
    
    # Ler arquivo Excel
    df = pd.read_excel(caminho_arquivo)
    print(f"Total de registros encontrados: {len(df)}")
    
    registros_importados = 0
    registros_com_erro = 0
    enderecos_substituidos = 0
    
    # Processar cada linha do Excel
    for index, row in df.iterrows():
        try:
            # Converter a data para formato Python
            data_str = row['data']
            if isinstance(data_str, str):
                try:
                    data = datetime.strptime(data_str, '%d/%m/%Y')
                except ValueError:
                    try:
                        data = datetime.strptime(data_str, '%Y-%m-%d')
                    except ValueError:
                        data = None
            else:
                data = data_str
            
            if data is None:
                print(f"Linha {index}: Data inválida. Pulando...")
                continue
            
            # Verificar se o CRAS existe pelo ID
            cras_id = row['cras_id'] if not pd.isna(row['cras_id']) else 1
            try:
                cras = CRAS.objects.get(id=cras_id)
            except CRAS.DoesNotExist:
                print(f"Linha {index}: CRAS ID {cras_id} não existe. Pulando...")
                continue
            
            # Verificar endereço e substituir se estiver vazio
            endereco = row['endereco']
            if pd.isna(endereco) or endereco == '':
                endereco = "Endereço não informado"
                enderecos_substituidos += 1
                print(f"Linha {index}: Endereço em branco substituído por valor padrão.")
            
            # Verificar se a ficha já existe
            numero_paif = row['numero_paif']
            ficha_existente = FichaPAIF.objects.filter(numero_paif=numero_paif).first()

            if ficha_existente:
                print(f"Ficha {numero_paif} já existe. Verificando atualizações...")
                
                # Lista de campos a verificar e atualizar se estiverem vazios
                campos_atualizaveis = {
                    'endereco': endereco if (pd.isna(ficha_existente.endereco) or ficha_existente.endereco == '') else ficha_existente.endereco,
                    'numero': row['numero'] if (not pd.isna(row['numero']) and (pd.isna(ficha_existente.numero) or ficha_existente.numero == '')) else ficha_existente.numero,
                    'bairro': row['bairro'] if (not pd.isna(row['bairro']) and (pd.isna(ficha_existente.bairro) or ficha_existente.bairro == '')) else ficha_existente.bairro,
                    'municipio': row['municipio'] if (not pd.isna(row['municipio']) and (pd.isna(ficha_existente.municipio) or ficha_existente.municipio == '')) else ficha_existente.municipio,
                }
                
                # Verificar se há algo para atualizar
                atualizacoes = False
                for campo, valor in campos_atualizaveis.items():
                    if getattr(ficha_existente, campo) != valor:
                        setattr(ficha_existente, campo, valor)
                        atualizacoes = True
                
                # Se houver atualizações, salvar o registro
                if atualizacoes:
                    try:
                        ficha_existente.save()
                        print(f"Ficha PAIF {numero_paif} atualizada com sucesso.")
                    except Exception as e:
                        print(f"Erro ao atualizar ficha PAIF: {e}")
                else:
                    print(f"Nenhuma atualização necessária para a ficha {numero_paif}.")
                
                # Verificar também se o beneficiário existe e precisa de atualização
                beneficiario_existente = Beneficiario.objects.filter(ficha_paif=ficha_existente).first()
                if beneficiario_existente:
                    # Lógica similar para atualizar o beneficiário
                    # ...
                
                    continue  # Pular para o próximo registro
            else:
                # Lidar com valores não numéricos em num_integrantes
                if pd.isna(row['num_integrantes']):
                    num_integrantes = 1  # Valor padrão
                elif isinstance(row['num_integrantes'], str) and row['num_integrantes'] == 'Não informado':
                    num_integrantes = 1  # Valor padrão para "Não informado"
                else:
                    try:
                        num_integrantes = int(row['num_integrantes'])
                    except (ValueError, TypeError):
                        num_integrantes = 1  # Valor padrão para erro de conversão
                
                # Criar ficha PAIF com campos obrigatórios
                ficha = FichaPAIF(
                    numero_paif=numero_paif,
                    tipo='inclusao',  # Valor padrão
                    data=data,
                    nome_referencia=row['responsavel_familiar'],
                    cpf='00000000000',  # Valor temporário, deve ser substituído pelo valor real
                    endereco=endereco,  # Agora usa o endereço tratado
                    numero=row['numero'] if not pd.isna(row['numero']) else '',
                    bairro=row['bairro'] if not pd.isna(row['bairro']) else 'Não informado',
                    cep='00000000',  # Valor temporário, deve ser substituído pelo valor real
                    municipio=row['municipio'] if not pd.isna(row['municipio']) else 'Não informado',
                    telefone='0000000000',  # Valor temporário, deve ser substituído pelo valor real
                    num_integrantes=num_integrantes,
                    cras=cras
                )
                
                try:
                    ficha.save()
                    print(f"Ficha PAIF {numero_paif} criada com sucesso.")
                except Exception as e:
                    print(f"Erro ao salvar ficha PAIF: {e}")
                    continue  # Pula para o próximo registro se houver erro
                
                # Criar beneficiário (pessoa responsável)
                # CORREÇÃO: remover campos inválidos para o modelo Beneficiario
                beneficiario = Beneficiario(
                    nome_completo=row['responsavel_familiar'],
                    data_nascimento=datetime(1900, 1, 1),  # Valor temporário
                    sexo='O',  # Valor temporário (Outro)
                    cpf='00000000000',  # Valor temporário, deve ser substituído pelo valor real
                    endereco=endereco,  # Usa o mesmo endereço tratado
                    nome_mae='Não informado',  # Valor temporário
                    ficha_paif=ficha,
                    cras=cras
                )
                
                try:
                    beneficiario.save()
                    print(f"Beneficiário {row['responsavel_familiar']} criado com sucesso.")
                    registros_importados += 1
                except Exception as e:
                    print(f"Erro ao salvar beneficiário: {e}")
                    # A ficha já foi salva, então não conta como erro total
                
                if registros_importados % 50 == 0:
                    print(f"Importados {registros_importados} registros...")
                
        except Exception as e:
            registros_com_erro += 1
            print(f"Erro ao importar linha {index}: {e}")
    
    print(f"\nImportação concluída!")
    print(f"Registros importados: {registros_importados}")
    print(f"Registros com erro: {registros_com_erro}")
    print(f"Endereços vazios substituídos: {enderecos_substituidos}")
    print("\nATENÇÃO: Os registros foram importados com alguns valores padrão para campos obrigatórios.")
    print("É necessário atualizar esses registros com as informações corretas depois.")

if __name__ == '__main__':
    # Caminho do seu arquivo Excel
    arquivo_excel = input("Digite o caminho completo do arquivo Excel: ")
    importar_dados_excel(arquivo_excel)