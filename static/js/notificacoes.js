/**
 * Sistema de Notificações do CRAS360
 * Versão simplificada para demonstração
 */

class NotificacaoManager {
    constructor() {
        // Inicializar com WebSocket simulado
        this.socket = this.criarWebSocketSimulado();
        
        // Contador de notificações
        this.contadorNotificacoes = 0;
        
        // Histórico de notificações
        this.historicoNotificacoes = [];
        
        console.log('Sistema de notificações inicializado (modo demonstração)');
    }
    
    criarWebSocketSimulado() {
        // Criamos um objeto que simula um WebSocket para demonstração
        console.log('WebSocket simulado criado - o endpoint real ainda não está configurado');
        
        return {
            // Simulação de métodos
            send: (dados) => {
                console.log('Simulando envio via WebSocket:', dados);
                
                // Simular recebimento da mesma mensagem (para demonstração)
                setTimeout(() => {
                    const data = JSON.parse(dados);
                    data.simulado = true;
                    this.processarNotificacao(data);
                    
                    // Alertar sobre WebSocket simulado
                    console.log('⚠️ Esta é apenas uma simulação. O WebSocket real precisa ser configurado.');
                }, 500);
            },
            close: () => console.log('WebSocket simulado fechado'),
            readyState: 1 // Simulando conexão aberta
        };
    }
    
    processarNotificacao(data) {
        // Verificar se a notificação é para o usuário atual
        if (window.USER_ID && data.tecnico_id && data.tecnico_id !== window.USER_ID && !data.para_todos) {
            return;
        }
        
        // Adicionar ao histórico
        this.historicoNotificacoes.unshift(data);
        if (this.historicoNotificacoes.length > 20) {
            this.historicoNotificacoes.pop();
        }
        
        // Atualizar contador
        this.contadorNotificacoes++;
        this.atualizarBadgeNotificacoes();
        
        // Exibir notificação
        this.exibirNotificacaoVisual(data);
        
        // Reproduzir som de notificação se disponível
        this.reproduzirSomNotificacao(data.tipo_notificacao);
    }
    
    exibirNotificacaoVisual(notificacao) {
        // Criar elemento de notificação
        const toast = document.createElement('div');
        toast.className = 'toast-notificacao';
        
        // Definir classe baseada no tipo
        let classeNotificacao = 'notificacao-padrao';
        let icone = 'fas fa-bell';
        
        switch (notificacao.tipo_notificacao) {
            case 'atendimento_aguardando':
                icone = 'fas fa-user-clock';
                break;
            case 'urgente':
                classeNotificacao = 'notificacao-urgente';
                icone = 'fas fa-exclamation-triangle';
                break;
            case 'informacao':
                classeNotificacao = 'notificacao-info';
                icone = 'fas fa-info-circle';
                break;
        }
        
        toast.classList.add(classeNotificacao);
        
        // Preencher conteúdo da notificação
        toast.innerHTML = `
            <div class="notificacao-cabecalho">
                <i class="${icone}"></i>
                <span>${notificacao.tipo_notificacao === 'urgente' ? 'URGENTE' : 'Notificação'}</span>
                <button class="notificacao-fechar">&times;</button>
            </div>
            <div class="notificacao-corpo">
                <p><strong>De:</strong> ${notificacao.origem || 'Sistema'}</p>
                ${notificacao.beneficiario ? `<p><strong>Beneficiário:</strong> ${notificacao.beneficiario}</p>` : ''}
                <p>${notificacao.mensagem}</p>
            </div>
            <div class="notificacao-rodape">
                ${this.formatarDataHora(notificacao.data_hora || new Date().toISOString())}
                ${notificacao.simulado ? '<small class="text-muted">(Demonstração)</small>' : ''}
            </div>
        `;
        
        // Adicionar à lista de notificações
        document.body.appendChild(toast);
        
        // Configurar botão de fechar
        toast.querySelector('.notificacao-fechar').addEventListener('click', () => {
            toast.remove();
        });
        
        // Remover depois de um tempo (exceto para urgentes)
        if (notificacao.tipo_notificacao !== 'urgente') {
            setTimeout(() => {
                if (document.body.contains(toast)) {
                    toast.classList.add('fadeout');
                    setTimeout(() => toast.remove(), 300);
                }
            }, 10000);
        }
    }
    
    reproduzirSomNotificacao(tipo) {
        try {
            console.log('Som de notificação seria reproduzido aqui');
            // Em uma implementação real, reproduziríamos o som
        } catch (e) {
            console.log('Aviso: Reprodução de som não suportada');
        }
    }
    
    enviarNotificacao(tecnicoId, tipo, beneficiario, mensagem) {
        if (!this.socket || this.socket.readyState !== 1) {
            console.error('Conexão WebSocket não está aberta.');
            return false;
        }
        
        const notificacao = {
            tipo: 'notificar_tecnico',
            tecnico_id: tecnicoId,
            tipo_notificacao: tipo || 'informacao',
            beneficiario: beneficiario,
            mensagem: mensagem,
            origem: window.USER_NOME || 'Sistema',
            data_hora: new Date().toISOString()
        };
        
        this.socket.send(JSON.stringify(notificacao));
        return true;
    }
    
    atualizarBadgeNotificacoes() {
        const badge = document.getElementById('badge-notificacoes');
        if (badge) {
            badge.textContent = this.contadorNotificacoes;
            badge.style.display = this.contadorNotificacoes > 0 ? 'inline-block' : 'none';
        }
    }
    
    formatarDataHora(dataHoraISO) {
        try {
            const data = new Date(dataHoraISO);
            return data.toLocaleString('pt-BR', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (e) {
            return new Date().toLocaleString('pt-BR');
        }
    }
    
    obterHistorico() {
        return this.historicoNotificacoes;
    }
    
    limparContador() {
        this.contadorNotificacoes = 0;
        this.atualizarBadgeNotificacoes();
    }
}

// Inicializar o gerenciador de notificações quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa o sistema de notificações e o torna disponível globalmente
    window.notificacoes = new NotificacaoManager();
});
