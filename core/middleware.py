import logging
from django.http import HttpResponseServerError
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class AdminLoginErrorMiddleware(MiddlewareMixin):
    """Middleware para capturar e tratar erros durante o login no Admin Django."""
    
    def process_exception(self, request, exception):
        # Verificar se a exceção ocorreu na página de login do admin
        if request.path == reverse('admin:login'):
            # Registrar o erro no log
            logger.error(f"Erro durante login no admin: {str(exception)}")
            
            # Verificar se é uma requisição POST (tentativa de login)
            if request.method == 'POST':
                # Criar uma resposta personalizada para o erro
                context = {
                    'title': 'Erro de Autenticação',
                    'error_message': 'Ocorreu um erro ao processar seu login. Por favor, verifique suas credenciais e tente novamente.',
                    'exception_type': type(exception).__name__,
                    'exception': str(exception),
                }
                
                # Retornar uma página de erro personalizada
                return TemplateResponse(
                    request, 
                    'admin/login_error.html',
                    context,
                    status=500
                )
        
        # Para outras exceções, deixar o Django lidar normalmente
        return None