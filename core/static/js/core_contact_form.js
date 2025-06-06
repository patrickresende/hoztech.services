document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitButton = form.querySelector('button[type="submit"]');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    const formFields = form.querySelectorAll('input, textarea');

    // Função para mostrar mensagem de erro
    function showError(message) {
        const errorSpan = errorMessage.querySelector('span');
        errorSpan.textContent = message;
        errorMessage.classList.remove('hidden');
        setTimeout(() => {
            errorMessage.classList.add('hidden');
        }, 5000);
    }

    // Função para mostrar mensagem de sucesso
    function showSuccess(message) {
        const successSpan = successMessage.querySelector('span');
        successSpan.textContent = message;
        successMessage.classList.remove('hidden');
        setTimeout(() => {
            successMessage.classList.add('hidden');
        }, 5000);
    }

    // Função para validar email
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Função para validar telefone
    function isValidPhone(phone) {
        const phoneRegex = /^\(\d{2}\) \d{5}-\d{4}$/;
        return phoneRegex.test(phone);
    }

    // Função para formatar telefone
    function formatPhoneNumber(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 0) {
            value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
            if (value.length > 9) {
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }
        }
        input.value = value;
    }

    // Adiciona máscara de telefone
    const phoneInput = form.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    }

    // Função para obter mensagem de erro específica para cada campo
    function getFieldErrorMessage(field) {
        const value = field.value.trim();
        
        if (value === '') {
            return `O campo ${field.name} é obrigatório`;
        }

        switch(field.name) {
            case 'name':
                if (value.length < 3) {
                    return 'O nome deve ter pelo menos 3 caracteres';
                }
                if (!/^[A-Za-zÀ-ÿ\s]{3,50}$/.test(value)) {
                    return 'O nome deve conter apenas letras e espaços';
                }
                break;
            case 'email':
                if (!isValidEmail(value)) {
                    return 'Por favor, insira um email válido';
                }
                break;
            case 'phone':
                if (!isValidPhone(value)) {
                    return 'O telefone deve estar no formato (99) 99999-9999';
                }
                break;
            case 'subject':
                if (value.length > 20) {
                    return 'O assunto deve ter no máximo 20 caracteres';
                }
                break;
            case 'message':
                if (value.length === 0) {
                    return 'A mensagem é obrigatória';
                }
                if (value.length > 5000) {
                    return 'A mensagem deve ter no máximo 5000 caracteres';
                }
                break;
        }
        return null;
    }

    // Validação em tempo real
    formFields.forEach(field => {
        if (field.name === 'website') return; // Ignora o campo honeypot

        field.addEventListener('blur', function() {
            validateField(this);
        });

        field.addEventListener('input', function() {
            if (this.classList.contains('border-red-500')) {
                validateField(this);
            }
        });
    });

    function validateField(field) {
        const errorMessage = getFieldErrorMessage(field);
        const feedbackElement = field.nextElementSibling;
        
        if (errorMessage) {
            field.classList.add('border-red-500');
            if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                feedbackElement.textContent = errorMessage;
                feedbackElement.style.display = 'block';
            }
            return false;
        }
        
        field.classList.remove('border-red-500');
        if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
            feedbackElement.style.display = 'none';
        }
        return true;
    }

    // Manipulação do envio do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Esconde mensagens anteriores
        successMessage.classList.add('hidden');
        errorMessage.classList.add('hidden');

        // Validação de todos os campos
        let isValid = true;
        let firstInvalidField = null;

        formFields.forEach(field => {
            if (field.name === 'website') return; // Ignora o campo honeypot
            
            if (!validateField(field)) {
                isValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });

        if (!isValid) {
            // Mostra mensagem de erro para o primeiro campo inválido
            const errorMessage = getFieldErrorMessage(firstInvalidField);
            showError(errorMessage);
            firstInvalidField.focus();
            return;
        }

        // Desabilita o botão e mostra o spinner
        submitButton.disabled = true;
        loadingSpinner.classList.remove('hidden');

        try {
            const formData = new FormData(form);
            const response = await fetch('/contato/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                showSuccess(data.message || 'Mensagem enviada com sucesso!');
                form.reset();
                formFields.forEach(field => {
                    field.classList.remove('border-red-500');
                    const feedbackElement = field.nextElementSibling;
                    if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                        feedbackElement.style.display = 'none';
                    }
                });
            } else {
                if (data.errors) {
                    // Mostra erros específicos do servidor
                    Object.entries(data.errors).forEach(([field, error]) => {
                        const input = form.querySelector(`[name="${field}"]`);
                        if (input) {
                            input.classList.add('border-red-500');
                            const feedbackElement = input.nextElementSibling;
                            if (feedbackElement && feedbackElement.classList.contains('invalid-feedback')) {
                                feedbackElement.textContent = error;
                                feedbackElement.style.display = 'block';
                            }
                        }
                    });
                    showError(data.message || 'Por favor, corrija os erros no formulário.');
                } else {
                    showError(data.message || 'Erro ao enviar mensagem. Por favor, tente novamente.');
                }
            }
        } catch (error) {
            console.error('Erro:', error);
            showError('Erro ao enviar mensagem. Por favor, tente novamente.');
        } finally {
            // Reabilita o botão e esconde o spinner
            submitButton.disabled = false;
            loadingSpinner.classList.add('hidden');
        }
    });
}); 