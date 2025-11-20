document.addEventListener("DOMContentLoaded", function() {
    // Carregar dados do backend
    const dadosBackendElement = document.getElementById('dados-backend');
    let dadosBackend = {};
    
    if (dadosBackendElement) {
        try {
            dadosBackend = JSON.parse(dadosBackendElement.textContent);
            console.log("Dados backend carregados:", dadosBackend);
        } catch (e) {
            console.error("Erro ao parsear dados do backend:", e);
        }
    }
    
    // Preencher os campos de data e CRAS
    document.getElementById('data_atendimento').value = new Date().toISOString().split('T')[0];
    
    // Configurar o histórico de evoluções
    const historicoContainer = document.getElementById('historicoContainer');
    if (historicoContainer && dadosBackend.evolucoes) {
        // Preencher histórico com dados do backend
        const evolucoes = JSON.parse(dadosBackend.evolucoes);
        
        evolucoes.forEach(evolucao => {
            const card = criarCartaoEvolucao(evolucao);
            historicoContainer.appendChild(card);
        });
    }
    
    // Adicionar evento para o botão de adicionar evolução
    const btnAdicionarEvolucao = document.getElementById('btn-adicionar-evolucao');
    if (btnAdicionarEvolucao) {
        btnAdicionarEvolucao.addEventListener('click', adicionarNovaEvolucao);
    }
    
    // Adicionar evento para o botão de registrar alteração na composição familiar
    const btnRegistrarAlteracao = document.getElementById('btn-registrar-alteracao');
    if (btnRegistrarAlteracao) {
        btnRegistrarAlteracao.addEventListener('click', registrarAlteracaoFamiliar);
    }
    
    // Função para criar um cartão de evolução
    function criarCartaoEvolucao(evolucao) {
        const card = document.createElement('div');
        card.className = 'evolucao-card';
        card.dataset.id = evolucao.id;
        
        card.innerHTML = `
            <div class="evolucao-header" onclick="toggleEvolucao(this)">
                <div class="evolucao-header-info">
                    <div class="evolucao-data">${evolucao.data}</div>
                    <div class="evolucao-tecnico">Técnico: ${evolucao.tecnico}</div>
                    <div class="evolucao-cras">CRAS: ${evolucao.cras}</div>
                </div>
                <button class="evolucao-toggle">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="evolucao-body">
                <div class="evolucao-description">${evolucao.descricao}</div>
                <div class="evolucao-actions">
                    <button class="btn btn-edit" onclick="editarEvolucao(${evolucao.id})">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-delete" onclick="excluirEvolucao(${evolucao.id})">
                        <i class="fas fa-trash-alt"></i> Excluir
                    </button>
                </div>
            </div>
        `;
        
        return card;
    }
    
    // Função para adicionar uma nova evolução
    function adicionarNovaEvolucao() {
        const descricao = document.getElementById('descricao_evolucao').value;
        
        if (!descricao.trim()) {
            alert("Por favor, preencha a descrição do atendimento");
            return;
        }
        
        const dados = {
            data_atendimento: document.getElementById('data_atendimento').value || new Date().toISOString().split('T')[0],
            tecnico: document.getElementById('nome_tecnico').value,
            cras: document.getElementById('cras').value,
            numero_paif: document.getElementById('numero_paif').value,
            descricao: descricao
        };
        
        // Enviar dados para a API
        fetch('/paif/api/evolucao-adicionar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dados)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Adicionar nova evolução ao histórico
                const historicoContainer = document.getElementById('historicoContainer');
                const card = criarCartaoEvolucao(data.evolucao);
                historicoContainer.insertBefore(card, historicoContainer.firstChild);
                
                // Limpar campo de descrição
                document.getElementById('descricao_evolucao').value = '';
                
                alert("Atendimento registrado com sucesso!");
            } else {
                alert("Erro ao registrar atendimento: " + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao registrar atendimento. Verifique sua conexão.");
        });
    }
    
    // Função para registrar alteração na composição familiar
    function registrarAlteracaoFamiliar() {
        const membros = [];
        const linhas = document.querySelectorAll('#familiaTable tbody tr:not(.expandable)');
        
        linhas.forEach(linha => {
            const nome = linha.querySelector('input[name="nome[]"]').value;
            
            if (nome.trim()) {
                const parentesco = linha.querySelector('input[name="parentesco[]"]').value;
                const dataNasc = linha.querySelector('input[name="data_nascimento[]"]').value;
                const idade = linha.querySelector('.idade-cell').textContent;
                
                const detalhes = linha.nextElementSibling;
                const frequenciaEscolar = detalhes.querySelector('select').value;
                const escola = detalhes.querySelectorAll('input')[0].value;
                const serie = detalhes.querySelectorAll('select')[2].value;
                const turno = detalhes.querySelectorAll('select')[1].value;
                const situacaoTrabalho = detalhes.querySelectorAll('select')[2].value;
                const renda = detalhes.querySelectorAll('input')[1].value;
                
                membros.push({
                    nome, parentesco, dataNasc, idade, 
                    frequenciaEscolar, escola, serie, turno, 
                    situacaoTrabalho, renda
                });
            }
        });
        
        if (membros.length === 0) {
            alert("Adicione pelo menos um membro à família antes de registrar.");
            return;
        }
        
        const dados = {
            numero_paif: document.getElementById('numero_paif').value,
            membros: membros
        };
        
        // Enviar dados para a API
        fetch('/paif/api/membros-familiares-adicionar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dados)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Composição familiar registrada com sucesso!");
            } else {
                alert("Erro ao registrar composição familiar: " + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert("Erro ao registrar composição familiar. Verifique sua conexão.");
        });
    }
    
    // Função para obter o valor de um cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Função para alternar a exibição do conteúdo da evolução
function toggleEvolucao(header) {
    const card = header.closest('.evolucao-card');
    const body = card.querySelector('.evolucao-body');
    const icon = header.querySelector('.evolucao-toggle i');
    
    if (body.classList.contains('visible')) {
        body.classList.remove('visible');
        icon.className = 'fas fa-chevron-down';
    } else {
        body.classList.add('visible');
        icon.className = 'fas fa-chevron-up';
    }
}

// Função para editar uma evolução
function editarEvolucao(id) {
    alert("Funcionalidade de edição a ser implementada para evolução #" + id);
}

// Função para excluir uma evolução
function excluirEvolucao(id) {
    if (confirm("Tem certeza que deseja excluir esta evolução?")) {
        // Implementar lógica para excluir evolução
        alert("Funcionalidade de exclusão a ser implementada para evolução #" + id);
    }
}

// Função para calcular idade a partir da data de nascimento
function calcularIdade(input) {
    const dataNasc = new Date(input.value);
    if (!isNaN(dataNasc.getTime())) {
        const hoje = new Date();
        let idade = hoje.getFullYear() - dataNasc.getFullYear();
        const m = hoje.getMonth() - dataNasc.getMonth();
        
        if (m < 0 || (m === 0 && hoje.getDate() < dataNasc.getDate())) {
            idade--;
        }
        
        const linha = input.closest('tr');
        const idadeCell = linha.querySelector('.idade-cell');
        idadeCell.textContent = idade;
    }
}

// Função para formatar valor monetário
function formatarParaReal(campo) {
    let valor = campo.value.replace(/\D/g, "");
    valor = (valor / 100).toFixed(2);
    valor = valor.replace(".", ",");
    campo.value = "R$ " + valor;
}
