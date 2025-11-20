# CRAS360 Demo - Guia Passo a Passo

A **Demo do CRAS360** foi finalizada com sucesso e populada com dados de exemplo. Este documento guia você sobre como rodar o projeto e acessar as funcionalidades.

## 🚀 Começando

O projeto está configurado e pronto para rodar. Todas as dependências foram instaladas e o banco de dados está populado.

### 1. Rodar o Servidor

Abra um terminal no diretório do projeto (`e:\Documentos\CODE_MODE-DEMO\cras360appweb_demo\cras360appweb_demo`) e execute:

```bash
python manage.py runserver
```

Acesse a aplicação em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🔑 Credenciais de Login

Para facilitar a demonstração, todos os perfis utilizam a mesma senha padrão.

**Senha Padrão:** `demo@cras360`

| Perfil | Email | Senha | Status |
| :--- | :--- | :--- | :--- |
| **Recepção** | `recepcao@cras360.com` | `demo@cras360` | ✅ Liberado |
| **Técnico Pedagogo** | `tecnico@cras360.com` | `demo@cras360` | ✅ Liberado |
| **Administrador** | `admin@cras360.com` | `demo@cras360` | ⚠️ Acesso Irrestrito |

> **Nota:** Outros perfis foram desativados ou ocultados nesta versão de demonstração para focar nas funcionalidades principais.

## ✨ Funcionalidades Principais para Explorar

### 1. Dashboard
- Faça login como **Recepção** para ver a visão específica de recepção.

### 2. PAIF (Atenção à Família)
- Navegue até o módulo **PAIF**.
- Você verá uma lista de famílias geradas pelo script de demonstração.
- Clique em uma família para ver detalhes (composição, endereço, status de vulnerabilidade).

### 3. Beneficiários
- Pesquise por beneficiários por nome ou CPF.
- O sistema inclui lógica de validação (embora simplificada para a demo).

## 🛠️ Notas Técnicas

- **Versão Demo**: Um banner foi adicionado ao topo para indicar claramente que se trata de uma versão de portfólio.
- **Versão do Django**: Atualizado para **Django 5.2.8** para suportar Python 3.13.
- **Banco de Dados**: SQLite (populado com dados sintéticos).

> [!TIP]
> Para resetar o banco de dados ou criar mais dados, você pode deletar o arquivo `db.sqlite3` e rodar os scripts de configuração novamente:
> ```bash
> python manage.py migrate
> python create_default_users.py
> python create_admin.py
> python create_demo_data.py
> ```
