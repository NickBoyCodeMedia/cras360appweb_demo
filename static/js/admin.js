/**
 * Funções para o módulo administrativo do CRAS360
 */

// Função para gerar documento Word
function gerarDocumentoWord(tipo, dados) {
    console.log(`Gerando documento Word do tipo: ${tipo}`);
    
    // Em uma implementação real, isso enviaria uma requisição AJAX
    // para o backend gerar o documento e retornar para download
    return fetch('/admin/api/gerar-documento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tipo: tipo,
            formato: 'word',
            dados: dados
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao gerar documento');
        }
        return response.blob();
    })
    .then(blob => {
        // Criar um link para download e clicar nele automaticamente
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.docx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao gerar documento: ' + error.message);
    });
}

// Função para gerar planilha Excel
function gerarPlanilhaExcel(tipo, dados) {
    console.log(`Gerando planilha Excel do tipo: ${tipo}`);
    
    // Em uma implementação real, isso enviaria uma requisição AJAX
    // para o backend gerar a planilha e retornar para download
    return fetch('/admin/api/gerar-documento', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            tipo: tipo,
            formato: 'excel',
            dados: dados
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao gerar planilha');
        }
        return response.blob();
    })
    .then(blob => {
        // Criar um link para download e clicar nele automaticamente
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${tipo}_${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao gerar planilha: ' + error.message);
    });
}

// Função para buscar funcionários do CRAS
function buscarFuncionarios() {
    return fetch('/admin/api/funcionarios')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar funcionários');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Erro:', error);
            return []; // Retorna array vazio em caso de erro
        });
}

// Função para gerar lista de frequência
function gerarListaFrequencia(formato, periodo, data) {
    console.log(`Gerando lista de frequência em formato ${formato} para o período ${periodo}`);
    
    // Coletar dados da tabela de frequência
    const tabela = document.getElementById(`tabela-frequencia-${periodo.toLowerCase()}`);
    if (!tabela) {
        alert('Tabela de frequência não encontrada!');
        return;
    }
    
    // Extrair dados da tabela
    const linhas = tabela.querySelectorAll('tbody tr');
    const funcionarios = Array.from(linhas).map(linha => {
        const colunas = linha.querySelectorAll('td');
        return {
            nome: colunas[0].textContent,
            cargo: colunas[1].textContent,
            entrada: colunas[2].textContent,
            saida: colunas[3].textContent
        };
    });
    
    const observacoes = document.getElementById('observacoes')?.value || '';
    
    // Dados a serem enviados para o servidor
    const dados = {
        data: data || new Date().toISOString().split('T')[0],
        periodo: periodo,
        funcionarios: funcionarios,
        observacoes: observacoes,
        cras: document.getElementById('cras-nome')?.value || 'CRAS SANTA CRUZ'
    };
    
    // Chamar a função adequada conforme o formato
    if (formato === 'word') {
        return gerarDocumentoWord('frequencia', dados);
    } else if (formato === 'excel') {
        return gerarPlanilhaExcel('frequencia', dados);
    }
}

// Função para salvar a frequência do dia
function salvarFrequencia(periodo, data) {
    console.log(`Salvando frequência do período ${periodo} da data ${data}`);
    
    const tabela = document.getElementById(`tabela-frequencia-${periodo.toLowerCase()}`);
    if (!tabela) {
        alert('Tabela de frequência não encontrada!');
        return;
    }
    
    // Extrair dados da tabela
    const linhas = tabela.querySelectorAll('tbody tr');
    const registros = Array.from(linhas).map(linha => {
        const colunas = linha.querySelectorAll('td');
        const funcionarioId = linha.dataset.funcionarioId;
        
        return {
            funcionario_id: funcionarioId,
            presente: true, // Por padrão, marcamos como presente se há dados de entrada/saída
            hora_entrada: colunas[2].textContent,
            hora_saida: colunas[3].textContent,
            observacoes: ''
        };
    });
    
    const observacoesGerais = document.getElementById('observacoes')?.value || '';
    
    // Dados a serem enviados para o servidor
    const dados = {
        data: data || new Date().toISOString().split('T')[0],
        periodo: periodo,
        registros: registros,
        observacoes: observacoesGerais
    };
    
    // Enviar para o servidor
    return fetch('/admin/api/salvar-frequencia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dados)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao salvar frequência');
        }
        return response.json();
    })
    .then(data => {
        alert('Frequência salva com sucesso!');
        return data;
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar frequência: ' + error.message);
    });
}

// Função para carregar funcionários na tabela de frequência
function carregarFuncionariosNaTabela(periodo) {
    console.log(`Carregando funcionários para o período ${periodo}`);
    
    buscarFuncionarios()
        .then(funcionarios => {
            if (!funcionarios || funcionarios.length === 0) {
                console.log('Nenhum funcionário encontrado, usando dados de exemplo');
                // Usar dados de exemplo caso não encontre funcionários
                return;
            }
            
            const tabela = document.getElementById(`tabela-frequencia-${periodo.toLowerCase()}`);
            if (!tabela) {
                console.error('Tabela não encontrada');
                return;
            }
            
            const tbody = tabela.querySelector('tbody');
            tbody.innerHTML = ''; // Limpar tabela
            
            // Preencher com funcionários da API
            funcionarios.forEach(funcionario => {
                // Determinar horários baseado no período e nos horários definidos para o funcionário
                let horarioEntrada = '';
                let horarioSaida = '';
                
                if (funcionario.horario_trabalho) {
                    const horarios = funcionario.horario_trabalho.split(',');
                    if (periodo === 'Manha' && horarios[0]) {
                        const [entrada, saida] = horarios[0].split('-');
                        horarioEntrada = entrada;
                        horarioSaida = saida;
                    } else if (periodo === 'Tarde' && horarios[1]) {
                        const [entrada, saida] = horarios[1].split('-');
                        horarioEntrada = entrada;
                        horarioSaida = saida;
                    }
                }
                
                const linha = document.createElement('tr');
                linha.dataset.funcionarioId = funcionario.id;
                
                linha.innerHTML = `
                    <td>${funcionario.nome_completo}</td>
                    <td>${funcionario.cargo}</td>
                    <td>${horarioEntrada}</td>
                    <td>${horarioSaida}</td>
                    <td class="assinatura-campo"></td>
                `;
                
                tbody.appendChild(linha);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar funcionários:', error);
        });
}

// Configurar eventos quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se estamos na página de frequência
    if (document.getElementById('tabela-frequencia-manha')) {
        // Carregar funcionários nas tabelas
        carregarFuncionariosNaTabela('Manha');
        carregarFuncionariosNaTabela('Tarde');
        
        // Botão para salvar frequência
        const btnSalvarFrequencia = document.getElementById('btn-salvar-frequencia');
        if (btnSalvarFrequencia) {
            btnSalvarFrequencia.addEventListener('click', function() {
                const periodo = document.querySelector('.nav-link.active').textContent.trim().includes('Manhã') ? 'Manha' : 'Tarde';
                const data = document.getElementById('data-frequencia').value;
                salvarFrequencia(periodo, data);
            });
        }
        
        // Botão de geração de documento Word
        const btnGerarWord = document.getElementById('btn-gerar-word');
        if (btnGerarWord) {
            btnGerarWord.addEventListener('click', function() {
                const periodo = document.querySelector('.nav-link.active').textContent.trim().includes('Manhã') ? 'Manha' : 'Tarde';
                const data = document.getElementById('data-frequencia').value;
                gerarListaFrequencia('word', periodo, data);
            });
        }
        
        // Botão de geração de planilha Excel
        const btnGerarExcel = document.getElementById('btn-gerar-excel');
        if (btnGerarExcel) {
            btnGerarExcel.addEventListener('click', function() {
                const periodo = document.querySelector('.nav-link.active').textContent.trim().includes('Manhã') ? 'Manha' : 'Tarde';
                const data = document.getElementById('data-frequencia').value;
                gerarListaFrequencia('excel', periodo, data);
            });
        }
    }
});
