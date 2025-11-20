/**
 * Conversor automático para maiúsculas
 * Converte automaticamente o conteúdo de campos de formulário para maiúsculas
 * exceto em formulários de login
 */
document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os elementos de formulário de texto
    const formElements = document.querySelectorAll('input[type="text"], input[type="search"], textarea');
    
    formElements.forEach(function(element) {
        // Verifica se o elemento está dentro de um formulário de login
        const isInLoginForm = isElementInLoginForm(element);
        
        if (!isInLoginForm) {
            // Adiciona evento para converter para maiúsculas durante digitação
            element.addEventListener('input', function() {
                const cursorPosition = this.selectionStart;
                this.value = this.value.toUpperCase();
                this.setSelectionRange(cursorPosition, cursorPosition);
            });
            
            // Converte valor inicial caso já exista
            if (element.value) {
                element.value = element.value.toUpperCase();
            }
        }
    });
    
    // Função para determinar se um elemento está em um formulário de login
    function isElementInLoginForm(element) {
        // Verifica pelos formulários ancestrais ou próprio elemento
        let currentNode = element;
        
        while (currentNode && currentNode !== document) {
            // Verifica se é um formulário de login por diferentes indicadores
            if (
                // Pelo ID
                (currentNode.id && (
                    currentNode.id.toLowerCase().includes('login') ||
                    currentNode.id.toLowerCase().includes('auth')
                )) ||
                // Pela classe
                (currentNode.className && (
                    currentNode.className.toLowerCase().includes('login') ||
                    currentNode.className.toLowerCase().includes('auth')
                )) ||
                // Pela action (para <form>)
                (currentNode.tagName === 'FORM' && currentNode.action && (
                    currentNode.action.toLowerCase().includes('login') ||
                    currentNode.action.toLowerCase().includes('auth') ||
                    currentNode.action.toLowerCase().includes('signin')
                )) ||
                // Pela URL da página (para páginas de login específicas)
                (window.location.pathname.includes('login') || 
                window.location.pathname.includes('auth'))
            ) {
                return true;
            }
            
            currentNode = currentNode.parentNode;
        }
        
        return false;
    }
});
