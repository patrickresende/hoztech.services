import logging
import traceback
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('core.admin')

class AdminLoginErrorMiddleware(MiddlewareMixin):
    """Middleware para capturar e tratar erros durante o login no Admin Django."""
    
    def process_exception(self, request, exception):
        # Verificar se a exceção ocorreu na página de login do admin
        if request.path.startswith('/admin/login'):
            # Registrar o erro no log com stack trace
            logger.error(f"[AUTH] Erro durante login no admin: {str(exception)}")
            logger.error(f"[AUTH] Stack trace: {traceback.format_exc()}")
            
            # Registrar informações adicionais
            logger.error(f"[AUTH] Método: {request.method}")
            logger.error(f"[AUTH] Usuário: {request.POST.get('username') if request.method == 'POST' else 'N/A'}")
            logger.error(f"[AUTH] Autenticado: {request.user.is_authenticated}")
            
            # Verificar se é uma requisição POST (tentativa de login)
            if request.method == 'POST':
                # Criar uma resposta personalizada para o erro
                context = {
                    'title': 'Erro de Autenticação',
                    'error_message': 'Ocorreu um erro ao processar seu login. Por favor, verifique suas credenciais e tente novamente.',
                    'exception_type': type(exception).__name__,
                    'exception': str(exception),
                    'debug': settings.DEBUG,
                    'username': request.POST.get('username', ''),
                    'auth_debug_url': reverse('core_admin:auth_debug'),
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