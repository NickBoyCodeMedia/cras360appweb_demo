"""
Módulo de configuração das coordenadas e layouts dos PDFs do S.I.L.V.I.A.
Contém todas as definições de posicionamento dos campos nos formulários.
"""

# Dicionário com os nomes dos arquivos de layout
LAYOUTS = {
    "Ficha Amarela": "layout_ficha_amarelo.jpg",
    "Ficha Azul": "layout_ficha_azul.jpg",
    "Ficha Verde": "layout_ficha_verde.jpg",
    "Ficha Vermelha": "layout_ficha_vermelha.jpg",
    "Som e Cidadania": "Som_e_Cidadania_layout.jpg",
    "Somos Tão Jovens": "Somos_tao_jovens_layout.jpg",
    "Nascer": "projeto_nascer_layout.jpg"
}

# Coordenadas dos campos em cada formulário
COORDENADAS = {
    "campos_projetos": {
        # Campos básicos para Som e Cidadania e Somos Tão Jovens
        "unidade": (85, 582),
        "data_cadastro": (497, 581),
        "nome": (85, 521),
        "sexo": (450, 521),
        "data_nascimento": (150, 502),
        "raca": (400, 502),
        "cpf": (53, 484),
        "rg": (220, 484),
        "orgao_emissor": (422, 484),
        "nis": (53, 467),
        "nome_mae": (100, 449),
        "contato": (85, 393),
        "endereco": (199, 323),
        "serie": (200, 220),
        "necessidades": (200, 240),
        "especificar": (200, 180),
        "checkboxes": {
            "paif": (200, 250),
            "paefi": (250, 250),
            "servico_acolhimento": (300, 250),
            "outros": (350, 250),
            "outros_especificar_check": (400, 250),
            "matriculado_sim": (450, 282),
            "matriculado_nao": (470, 282)
        }
    },
    "campos_fichas": {
        # Campos básicos para todas as fichas coloridas
        "unidade": (85, 582),
        "data_cadastro": (497, 581),
        "nome": (85, 521),
        "sexo": (450, 521),
        "data_nascimento": (150, 502),
        "raca": (400, 502),
        "cpf": (53, 484),
        "rg": (220, 484),
        "orgao_emissor": (422, 484),
        "nis": (53, 467),
        "nome_mae": (100, 449),
        "contato": (85, 393),
        "endereco": (199, 323),
        "numero": (85, 305),
        "bairro": (199, 305),
        "responsavel": (150, 280),
        "cpf_responsavel": (150, 260),
        "rg_responsavel": (280, 260),
        "orgao_responsavel": (400, 260),
        "checkboxes_prioridade": {
            "prioridade_nenhuma": (200, 240),
            "prioridade_isolamento": (250, 240),
            "prioridade_violencia": (300, 240),
            "prioridade_defasagem": (350, 240),
            "prioridade_acolhimento": (400, 240),
            "prioridade_socioeducativa": (450, 240),
            "prioridade_egressos": (200, 220),
            "prioridade_trabalho_infantil": (250, 220),
            "prioridade_abuso": (300, 220),
            "prioridade_eca": (350, 220),
            "prioridade_rua": (400, 220),
            "prioridade_deficiencia": (450, 220)
        },
        "checkboxes_renda": {
            "renda_bolsa_familia": (200, 200),
            "bpc_idoso": (250, 200),
            "bpc_pcd": (300, 200),
            "aposentadoria": (350, 200)
        }
    },
    "nascer": {
        # Campos básicos do Nascer
        "unidade": (85, 582),
        "data_cadastro": (497, 581),
        "nome": (85, 521),
        "sexo": (450, 521),
        "data_nascimento": (150, 502),
        "raca": (400, 502),
        "cpf": (53, 484),
        "rg": (220, 484),
        "orgao_emissor": (422, 484),
        "nis": (53, 467),
        "nome_mae": (100, 449),
        "contato": (85, 393),
        "endereco": (199, 323),
        "numero": (85, 305),
        "bairro": (199, 305),
        "num_pessoas_domicilio": (85, 285),
        "checkboxes": {
            "situacao_domicilio_proprio": (450, 282),
            "situacao_domicilio_alugado": (470, 282),
            "trabalho_formal_sim": (490, 282),
            "trabalho_formal_nao": (510, 282),
            "paif_nascer": (200, 250),
            "paefi_nascer": (250, 250),
            "participa_outras_nascer": (300, 250),
            "criança_feliz_nascer": (350, 250),
            "bolsa_familia_nascer": (200, 230),
            "bpc_pcd_nascer": (250, 230),
            "trabalho_informal_nascer": (300, 230)
        }
    }
}