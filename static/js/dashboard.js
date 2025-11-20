document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM completamente carregado e analisado.');

    // Declarar a variável no início do escopo
    let graficosInicializados = false;

    // Logs detalhados para depurar o problema de data-user-perfil
    console.log('Elemento HTML:', document.documentElement);
    console.log('Todos os atributos do elemento HTML:', document.documentElement.attributes);
    console.log('Dataset completo:', document.documentElement.dataset);
    
    // Verificar diretamente os atributos do elemento HTML
    const htmlAttributes = {};
    for (let attr of document.documentElement.attributes) {
        htmlAttributes[attr.name] = attr.value;
    }
    console.log('Atributos extraídos manualmente:', htmlAttributes);

    // Verificar se o atributo data-user-perfil está definido
    const userPerfil = document.documentElement.dataset.userPerfil;
    console.log('Valor de data-user-perfil:', userPerfil);
    
    // Verificar se os elementos do gráfico existem
    const chartPublicoElement = document.getElementById('chartPorPublico');
    const chartTipoElement = document.getElementById('chartPorTipo');
    
    function inicializarGraficos() {
        // Se já inicializou ou elementos não existem, não fazer nada
        if (graficosInicializados || !chartPublicoElement || !chartTipoElement) {
            return;
        }
        
        // Marcar como inicializado
        graficosInicializados = true;
        
        // Destruir instâncias existentes (se houver)
        if (window.chartPorPublico && typeof window.chartPorPublico.destroy === 'function') {
            window.chartPorPublico.destroy();
        }
        if (window.chartPorTipo && typeof window.chartPorTipo.destroy === 'function') {
            window.chartPorTipo.destroy();
        }
        
        try {
            const chartDataPublicoElement = document.getElementById('chartDataPublico');
            const chartDataAtendimentosElement = document.getElementById('chartDataAtendimentos');
            
            // DADOS FICTÍCIOS para uso quando os dados do backend não estão disponíveis
            const dadosFicticiosPublico = [
                {label: 'Crianças (0-12)', valor: 127},
                {label: 'Adolescentes (13-17)', valor: 98},
                {label: 'Adultos (18-59)', valor: 245},
                {label: 'Idosos (60+)', valor: 86}
            ];
            
            const dadosFicticiosAtendimentos = [
                {label: 'PAIF', valor: 187},
                {label: 'SCFV', valor: 142},
                {label: 'Benefícios', valor: 98},
                {label: 'Outros', valor: 53}
            ];
            
            // Tentar obter os dados do backend ou usar os fictícios
            let chartDataPublico = dadosFicticiosPublico;
            let chartDataAtendimentos = dadosFicticiosAtendimentos;
            
            // Tentar usar dados reais se disponíveis
            if (chartDataPublicoElement && chartDataAtendimentosElement) {
                try {
                    const dadosReaisPublico = JSON.parse(chartDataPublicoElement.textContent);
                    const dadosReaisAtendimentos = JSON.parse(chartDataAtendimentosElement.textContent);
                    
                    if (Array.isArray(dadosReaisPublico) && dadosReaisPublico.length > 0) {
                        chartDataPublico = dadosReaisPublico;
                    }
                    
                    if (Array.isArray(dadosReaisAtendimentos) && dadosReaisAtendimentos.length > 0) {
                        chartDataAtendimentos = dadosReaisAtendimentos;
                    }
                    
                    console.log('Usando dados reais para os gráficos');
                } catch (parseError) {
                    console.error('Erro ao analisar JSON, usando dados fictícios:', parseError);
                }
            } else {
                console.log('Elementos de dados não encontrados, usando dados fictícios');
            }

            // Configurar gráfico de distribuição por público
            window.chartPorPublico = new Chart(chartPublicoElement.getContext('2d'), {
                type: 'pie',
                data: {
                    labels: chartDataPublico.map(item => item.label),
                    datasets: [{
                        data: chartDataPublico.map(item => item.valor),
                        backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#6f42c1']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            // Configurar gráfico de atendimentos por tipo
            window.chartPorTipo = new Chart(chartTipoElement.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: chartDataAtendimentos.map(item => item.label),
                    datasets: [{
                        data: chartDataAtendimentos.map(item => item.valor),
                        backgroundColor: '#28a745'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });
            
            console.log('Gráficos inicializados com sucesso!');
        } catch (error) {
            console.error("Erro ao inicializar gráficos:", error);
        }
    }
    
    // Chamar a função para coordenador
    if (userPerfil === 'Coordenador') {
        inicializarGraficos();
    }
    
    // Também inicializar se os elementos existirem (independente do perfil)
    if (chartPublicoElement && chartTipoElement) {
        inicializarGraficos();
    }
});