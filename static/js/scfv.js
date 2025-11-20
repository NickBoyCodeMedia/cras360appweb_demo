document.addEventListener('DOMContentLoaded', function() {
    // Máscaras para campos
    if (typeof $.fn.mask === 'function') {
        $('.cpf').mask('000.000.000-00');
        $('.phone').mask('(00) 00000-0000');
        $('.date').mask('00/00/0000');
        $('.numeric').mask('0000000000');
    }

    // Converter texto para maiúsculas
    document.querySelectorAll('.uppercase').forEach(function(element) {
        element.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });

    // Função para alternar visibilidade do campo "outros"
    window.toggleOutros = function(checkbox) {
        document.getElementById('qual_outros').disabled = !checkbox.checked;
    }

    // Função para alternar visibilidade do campo "outras doenças"
    window.toggleOutrosDoencas = function(checkbox) {
        document.getElementById('quais_outras_doencas').disabled = !checkbox.checked;
    }

    // Função para alternar visibilidade dos dados do curador
    window.toggleCurador = function(checkbox) {
        document.getElementById('dados_curador').style.display = checkbox.checked ? 'block' : 'none';
    }

    // Navegação entre abas
    window.navegarParaAba = function(abaId) {
        document.querySelector('#myTab button[data-bs-target="#' + abaId + '"]').click();
    }
});
