// Função para trocar as moedas
function swapCurrencies() {
    const moedaEntrada = document.getElementById('moeda_entrada');
    const moedaSaida = document.getElementById('moeda_saida');
    
    // Trocar os valores
    const temp = moedaEntrada.value;
    moedaEntrada.value = moedaSaida.value;
    moedaSaida.value = temp;
    
    // Adicionar efeito visual
    const swapButton = document.querySelector('.swap-button');
    swapButton.style.transform = 'translateX(50%) rotate(180deg)';
    setTimeout(() => {
        swapButton.style.transform = 'translateX(50%) rotate(0deg)';
    }, 300);
}

// Função para inicializar eventos quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar loading state no formulário
    const form = document.getElementById('converterForm');
    if (form) {
        form.addEventListener('submit', function() {
            this.classList.add('loading');
            const button = this.querySelector('.convert-button');
            button.innerHTML = '<i class="fas fa-spinner"></i> Convertendo...';
        });
    }

    // Auto-dismiss error messages
    setTimeout(() => {
        const errorMessages = document.querySelectorAll('.flash-error');
        errorMessages.forEach(message => {
            message.style.animation = 'slideOut 0.5s ease forwards';
            setTimeout(() => message.remove(), 500);
        });
    }, 5000);

    // Validação em tempo real
    const valorInput = document.getElementById('valor_digitado');
    if (valorInput) {
        valorInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value <= 0) {
                this.setCustomValidity('O valor deve ser maior que zero');
            } else {
                this.setCustomValidity('');
            }
        });
    }
});