import logging
import traceback
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import DatabaseError, connection

logger = logging.getLogger('core.admin')

class AdminErrorMiddleware:
    """
    Middleware para capturar e tratar erros específicos do admin
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se é uma requisição do admin
        is_admin_request = (
            request.path.startswith('/admin/') or 
            request.path.startswith('/core_admin/')
        )
        
        if not is_admin_request:
            return self.get_response(request)
        
        try:
            # Testar conexão com banco antes de processar
            if not connection.ensure_connection():
                logger.error("Falha na conexão com banco de dados")
                if settings.DEBUG:
                    raise DatabaseError("Conexão com banco falhou")
                else:
                    return self._render_admin_error(
                        request, 
                        "Erro de conexão com banco de dados. Tente novamente em alguns instantes.",
                        "Database Connection Error"
                    )
            
            response = self.get_response(request)
            return response
            
        except DatabaseError as e:
            logger.error(f"Erro de banco de dados no admin: {e}")
            logger.error(traceback.format_exc())
            
            if settings.DEBUG:
                raise
            else:
                return self._render_admin_error(
                    request,
                    "Erro de banco de dados. Tente novamente em alguns instantes.",
                    "Database Error"
                )
                
        except PermissionDenied as e:
            logger.warning(f"Permissão negada no admin: {e}")
            if settings.DEBUG:
                raise
            else:
                return self._render_admin_error(
                    request,
                    "Você não tem permissão para acessar esta área.",
                    "Permission Denied"
                )
                
        except ValidationError as e:
            logger.warning(f"Erro de validação no admin: {e}")
            if settings.DEBUG:
                raise
            else:
                return self._render_admin_error(
                    request,
                    "Dados inválidos. Verifique as informações e tente novamente.",
                    "Validation Error"
                )
                
        except Exception as e:
            logger.error(f"Erro inesperado no admin: {e}")
            logger.error(traceback.format_exc())
            
            if settings.DEBUG:
                raise
            else:
                return self._render_admin_error(
                    request,
                    "Erro interno do servidor. Tente novamente em alguns instantes.",
                    "Internal Server Error"
                )

    def _render_admin_error(self, request, message, title):
        """Renderiza página de erro personalizada para o admin"""
        try:
            context = {
                'error_message': message,
                'error_title': title,
                'is_admin': True,
                'debug': settings.DEBUG,
            }
            
            html = render_to_string('admin/error.html', context, request=request)
            return HttpResponseServerError(html)
            
        except Exception as e:
            logger.error(f"Erro ao renderizar página de erro: {e}")
            # Fallback simples
            return HttpResponseServerError(
                f"<h1>{title}</h1><p>{message}</p>"
            )

class AdminPerformanceMiddleware:
    """
    Middleware para monitorar performance do admin
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se é uma requisição do admin
        is_admin_request = (
            request.path.startswith('/admin/') or 
            request.path.startswith('/core_admin/')
        )
        
        if not is_admin_request:
            return self.get_response(request)
        
        import time
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Log de performance para requisições lentas
        duration = time.time() - start_time
        if duration > 2.0:  # Mais de 2 segundos
            logger.warning(
                f"Requisição admin lenta: {request.path} levou {duration:.2f}s"
            )
        
        return response 