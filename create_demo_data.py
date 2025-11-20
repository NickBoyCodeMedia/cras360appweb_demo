import os
import django
import random
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cras360.settings')
django.setup()

from apps.core.models import Beneficiario, FichaPAIF, CRAS, Cidade

def create_demo_data():
    print("Creating demo data...")
    
    # Ensure Cidade exists
    cidade, created = Cidade.objects.get_or_create(
        nome="Cidade Demo",
        uf="SP"
    )

    # Ensure CRAS exists
    cras, created = CRAS.objects.get_or_create(
        nome="CRAS Centro",
        defaults={
            'endereco': 'Rua Principal, 100', 
            'telefone': '12345678',
            'cidade': cidade,
            'coordenador': 'Coordenador Demo'
        }
    )

    names = [
        "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", 
        "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho"
    ]
    first_names = [
        "Maria", "Jose", "Ana", "Joao", "Antonio", "Francisco", "Carlos", "Paulo",
        "Pedro", "Lucas", "Luiz", "Marcos", "Luis", "Gabriel", "Rafael", "Daniel"
    ]
    
    # Create FichaPAIF and Beneficiarios
    for i in range(20):
        numero_paif = f"2025{i:04d}"
        if FichaPAIF.objects.filter(numero_paif=numero_paif).exists():
            continue
            
        nome_familia = f"{random.choice(first_names)} {random.choice(names)}"
        
        ficha = FichaPAIF.objects.create(
            numero_paif=numero_paif,
            tipo='inclusao',
            data=datetime.now().date() - timedelta(days=random.randint(0, 365)),
            nome_referencia=nome_familia,
            cpf=f"{random.randint(10000000000, 99999999999)}",
            endereco=f"Rua {random.choice(names)}, {random.randint(1, 1000)}",
            numero=str(random.randint(1, 1000)),
            bairro="Centro",
            cep="12345000",
            municipio=cidade.nome,
            telefone="11999999999",
            num_integrantes=random.randint(1, 6),
            cras=cras
        )
        
        Beneficiario.objects.create(
            nome_completo=nome_familia,
            data_nascimento=datetime.now().date() - timedelta(days=random.randint(7000, 25000)),
            sexo=random.choice(['M', 'F']),
            cpf=ficha.cpf,
            endereco=ficha.endereco,
            nome_mae=f"Mae de {nome_familia}",
            ficha_paif=ficha,
            cras=cras
        )
        print(f"Created family: {nome_familia}")

    print("Demo data created successfully!")

if __name__ == '__main__':
    create_demo_data()
