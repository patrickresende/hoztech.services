import logging
import json
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

logger = logging.getLogger('core.admin')

def auth_debug_view(request):
    """
    View para exibir informações de depuração relacionadas à autenticação.
    """
    # Coletar dados da sessão de forma segura
    session_data = {}
    for key in request.session.keys():
        try:
            # Evitar expor dados sensíveis
            if key not in ['_auth_user_id', '_auth_user_backend', '_auth_user_hash']:
                session_data[key] = request.session[key]
            else:
                session_data[key] = '[PROTEGIDO]'
        except Exception as e:
            session_data[key] = f'[ERRO: {str(e)}]'
    
    # Registrar informações no log
    logger.info(f"Página de depuração de autenticação acessada por {request.user}")
    
    # Preparar contexto
    context = {
        'title': 'Depuração de Autenticação',
        'session_data': json.dumps(session_data, indent=2),
        'login_redirect_url': getattr(settings, 'LOGIN_REDIRECT_URL', None),
        'logout_redirect_url': getattr(settings, 'LOGOUT_REDIRECT_URL', None),
        'login_url': getattr(settings, 'LOGIN_URL', None),
        'debug': settings.DEBUG,
    }
    
    return render(request, 'admin/login_debug.html', context)