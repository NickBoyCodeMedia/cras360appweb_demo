/**
 * Script para gerenciar funcionalidades do módulo de relatórios
 */

// Função para inicializar a página de relatórios
function inicializarRelatorios() {
    console.log('Inicializando módulo de relatórios...');
    
    // Configurar manipuladores de eventos para seletores de tipos de relatório
    configurarSeletoresTipoRelatorio();
    
    // Configurar formatos de saída
    configurarFormatosSaida();
    
    // Inicializar datepickers e outros componentes
    inicializarComponentes();
    
    // Verificar permissões do usuário
    verificarPermissoes();
}

// Configurar manipuladores para os seletores de tipo de relatório
function configurarSeletoresTipoRelatorio() {
    const seletorTipo = document.getElementById('tipo_relatorio');
    if (!seletorTipo) return;
    
    seletorTipo.addEventListener('change', function() {
        atualizarCamposFiltro(this.value);
    });
    
    // Trigger inicial para configurar os campos corretos
    atualizarCamposFiltro(seletorTipo.value);
}

// Atualizar campos de filtro com base no tipo de relatório selecionado
function atualizarCamposFiltro(tipoRelatorio) {
    // Ocultar todos os filtros condicionais
    const filtrosCondicionais = document.querySelectorAll('[id^="filtro-"]');
    filtrosCondicionais.forEach(filtro => {
        filtro.style.display = 'none';
    });
    
    // Mostrar filtros específicos baseados no tipo
    switch(tipoRelatorio) {
        case 'cadastro':
            // Nada especial para mostrar
            break;
        case 'lista_projeto':
            document.getElementById('filtro-projeto')?.style.display = 'flex';
            break;
        case 'idade':
            document.getElementById('filtro-idade')?.style.display = 'flex';
            break;
        case 'lista_socioeconomica':
            document.getElementById('filtro-socioeconomico')?.style.display = 'flex';
            break;
        case 'frequencia':
            document.getElementById('filtro-frequencia')?.style.display = 'flex';
            break;
    }
}

// Configurar formatos de saída
function configurarFormatosSaida() {
    const seletorFormato = document.getElementById('formato');
    if (!seletorFormato) return;
    
    seletorFormato.addEventListener('change', function() {
        const btnEnviar = document.querySelector('button[type="submit"]');
        
        if (this.value === 'visualizar') {
            btnEnviar.textContent = 'Visualizar Relatório';
        } else if (this.value === 'pdf') {
            btnEnviar.textContent = 'Gerar PDF';
        } else if (this.value === 'excel') {
            btnEnviar.textContent = 'Exportar Excel';
        }
    });
}

// Inicializar componentes da página
function inicializarComponentes() {
    // Configurar datepickers
    const datepickers = document.querySelectorAll('input[type="date"]');
    datepickers.forEach(input => {
        if (!input.value) {
            const hoje = new Date();
            const dataFormatada = hoje.toISOString().split('T')[0];
            
            // Data inicial como primeiro dia do mês atual
            if (input.id === 'data_inicio') {
                const primeiroDia = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
                input.value = primeiroDia.toISOString().split('T')[0];
            } 
            // Data final como hoje
            else if (input.id === 'data_fim') {
                input.value = dataFormatada;
            }
        }
    });
    
    // Configurar checkboxes
    const checkboxes = document.querySelectorAll('input[name="colunas"]');
    const btnToggleAll = document.getElementById('toggle_all_columns');
    
    if (btnToggleAll) {
        btnToggleAll.addEventListener('click', function() {
            const checkAll = this.dataset.state === 'unchecked';
            checkboxes.forEach(checkbox => {
                checkbox.checked = checkAll;
            });
            
            this.dataset.state = checkAll ? 'checked' : 'unchecked';
            this.textContent = checkAll ? 'Desmarcar Todos' : 'Marcar Todos';
        });
    }
}

// Validar formulário antes do envio
function validarFormularioRelatorio(form) {
    // Verificar se pelo menos uma coluna está selecionada
    const colunasSelecionadas = form.querySelectorAll('input[name="colunas"]:checked');
    if (colunasSelecionadas.length === 0) {
        alert('Selecione pelo menos uma coluna para o relatório.');
        return false;
    }
    
    // Validações específicas para cada tipo de relatório
    const tipoRelatorio = form.querySelector('#tipo_relatorio').value;
    
    if (tipoRelatorio === 'idade') {
        const idadeMin = form.querySelector('#idade_min').value;
        const idadeMax = form.querySelector('#idade_max').value;
        
        if (idadeMin && idadeMax && parseInt(idadeMin) > parseInt(idadeMax)) {
            alert('A idade mínima não pode ser maior que a idade máxima.');
            return false;
        }
    }
    
    if (tipoRelatorio === 'lista_socioeconomica') {
        const rendaMin = form.querySelector('#renda_minima').value;
        const rendaMax = form.querySelector('#renda_maxima').value;
        
        if (rendaMin && rendaMax && parseFloat(rendaMin) > parseFloat(rendaMax)) {
            alert('A renda mínima não pode ser maior que a renda máxima.');
            return false;
        }
    }
    
    // Validar datas
    const dataInicio = form.querySelector('#data_inicio').value;
    const dataFim = form.querySelector('#data_fim').value;
    
    if (dataInicio && dataFim && new Date(dataInicio) > new Date(dataFim)) {
        alert('A data inicial não pode ser posterior à data final.');
        return false;
    }
    
    return true;
}

// Função para exibir o relatório na tela
function exibirRelatorioNaTela(data) {
    const cabecalho = document.getElementById('tabela-cabecalho');
    const corpo = document.getElementById('tabela-corpo');
    const container = document.getElementById('relatorio-resultado');
    
    // Limpar tabela
    cabecalho.innerHTML = '';
    corpo.innerHTML = '';
    
    // Verificar se há dados para exibir
    if (!data.resultados || data.resultados.length === 0) {
        const mensagem = document.createElement('tr');
        mensagem.innerHTML = `<td colspan="${data.colunas.length}" class="text-center">Nenhum registro encontrado com os filtros aplicados.</td>`;
        corpo.appendChild(mensagem);
    } else {
        // Adicionar cabeçalhos
        data.colunas.forEach(coluna => {
            const th = document.createElement('th');
            th.textContent = coluna;
            cabecalho.appendChild(th);
        });
        
        // Adicionar dados
        data.resultados.forEach(registro => {
            const tr = document.createElement('tr');
            
            data.colunas.forEach(coluna => {
                const td = document.createElement('td');
                const chave = coluna.toLowerCase().replace(' ', '_');
                td.textContent = registro[chave] || '';
                tr.appendChild(td);
            });
            
            corpo.appendChild(tr);
        });
        
        // Adicionar resumo e estatísticas se disponíveis
        if (data.resumo) {
            const divResumo = document.createElement('div');
            divResumo.className = 'mt-4 p-3 bg-light';
            divResumo.innerHTML = `<h5>Resumo</h5><p>${data.resumo}</p>`;
            container.appendChild(divResumo);
        }
    }
    
    // Exibir o container do relatório
    container.style.display = 'block';
    
    // Rolar para o relatório
    container.scrollIntoView({ behavior: 'smooth' });
}

// Função para verificar permissões do usuário e ajustar a interface
function verificarPermissoes() {
    // Obter o tipo de relatório da URL atual
    const url = window.location.href;
    let tipoRelatorio = null;
    
    if (url.includes('/relatorios/scfv/')) {
        tipoRelatorio = 'scfv';
    } else if (url.includes('/relatorios/paif/')) {
        tipoRelatorio = 'paif';
    }
    
    // Se estamos em uma página específica de relatório, verificar acesso via API
    if (tipoRelatorio) {
        fetch(`/relatorios/verificar-permissao/${tipoRelatorio}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Se o usuário não tem permissão, redirecionar para a página inicial
            if (!data.tem_permissao) {
                alert('Você não tem permissão para acessar este relatório.');
                window.location.href = '/relatorios/';
            }
        })
        .catch(error => {
            console.error('Erro ao verificar permissões:', error);
        });
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', inicializarRelatorios);

// Evento de submissão para validação
document.querySelectorAll('form[id$="-filtros-form"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!validarFormularioRelatorio(this)) {
            e.preventDefault();
        }
    });
});
