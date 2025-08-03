import logging
import time
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings

logger = logging.getLogger('core.admin')

class AdminLoginRedirectMiddleware(MiddlewareMixin):
    """
    Middleware para garantir que após o login bem-sucedido no admin,
    o usuário seja redirecionado para o dashboard do admin.
    """
    
    def process_request(self, request):
        # Registrar informações sobre a requisição para depuração
        if request.path.startswith('/admin/login'):
            logger.info(f"[AUTH] Requisição para {request.path} - Método: {request.method} - Usuário autenticado: {request.user.is_authenticated}")
            if request.method == 'POST':
                logger.info(f"[AUTH] Tentativa de login - Usuário: {request.POST.get('username')}")
        return None
    
    def process_response(self, request, response):
        # Verificar se é uma resposta de redirecionamento após login bem-sucedido
        if (request.path.startswith('/admin/login') and 
            request.method == 'POST' and 
            response.status_code == 302):
            
            # Verificar se o usuário está autenticado
            if request.user.is_authenticated:
                logger.info(f"[AUTH] Usuário {request.user.username} autenticado com sucesso. Redirecionando para o dashboard.")
                
                # Verificar se há um 'next' na requisição
                next_url = request.POST.get(REDIRECT_FIELD_NAME)
                if next_url:
                    logger.info(f"[AUTH] Redirecionando para next_url: {next_url}")
                    return HttpResponseRedirect(next_url)
                
                # Usar a configuração LOGIN_REDIRECT_URL ou o dashboard do admin como fallback
                redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', reverse('admin:index'))
                logger.info(f"[AUTH] Redirecionando para: {redirect_url}")
                
                # Pequeno atraso para garantir que a sessão seja salva
                time.sleep(0.1)
                
                # Redirecionar para o dashboard do admin
                return HttpResponseRedirect(redirect_url)
            else:
                logger.warning(f"[AUTH] Redirecionamento após POST, mas usuário não está autenticado. URL: {response.get('Location')}")
        
        return response