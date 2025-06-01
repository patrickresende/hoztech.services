from django.shortcuts import render
from django.http import FileResponse, JsonResponse
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import re
import os
import logging
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass
from functools import wraps
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .forms import ContactForm
import time
from django.views.generic import ListView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
import json
import csv
import xlsxwriter
from io import BytesIO
import zipfile

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Data class to hold validation results"""
    is_valid: bool
    error_message: Optional[str] = None

class InputValidator:
    """Class to handle input validation with regex patterns"""
    
    # Regex patterns
    NAME_PATTERN = r'^[A-Za-zÀ-ÿ\s]{3,50}$'
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^\d{8,15}$'
    DANGEROUS_CONTENT_PATTERN = r'<script|javascript:|on\w+\s*=|data:'
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input to prevent XSS and other attacks"""
        if not text:
            return ""
        # Remove HTML tags and potentially dangerous content
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'[\\<>]', '', text)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'on\w+=', '', text)
        return text.strip()
    
    @classmethod
    def validate_name(cls, name: str) -> ValidationResult:
        """Validate name format and length"""
        if not name or not isinstance(name, str):
            return ValidationResult(False, "Nome inválido")
        
        if not re.match(cls.NAME_PATTERN, name):
            return ValidationResult(False, "O nome deve conter apenas letras e espaços (3-50 caracteres)")
        
        return ValidationResult(True)
    
    @classmethod
    def validate_email(cls, email: str) -> ValidationResult:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return ValidationResult(False, "Email inválido")
        
        if not re.match(cls.EMAIL_PATTERN, email):
            return ValidationResult(False, "Formato de email inválido")
        
        return ValidationResult(True)
    
    @classmethod
    def validate_phone(cls, phone: str) -> ValidationResult:
        """Validate phone number format"""
        if not phone or not isinstance(phone, str):
            return ValidationResult(False, "Telefone inválido")
        
        if not re.match(cls.PHONE_PATTERN, phone):
            return ValidationResult(False, "O telefone deve conter apenas números (8-15 dígitos)")
        
        return ValidationResult(True)
    
    @classmethod
    def validate_subject(cls, subject: str) -> ValidationResult:
        """Validate subject length and content"""
        if not subject:
            return ValidationResult(False, "O assunto é obrigatório")
        
        if len(subject) > 20:
            return ValidationResult(False, "O assunto deve ter no máximo 20 caracteres")
        
        return ValidationResult(True)
    
    @classmethod
    def validate_message(cls, message: str) -> ValidationResult:
        """Validate message content and length"""
        if not message or not isinstance(message, str):
            return ValidationResult(False, "Mensagem inválida")
        
        if len(message) > 5000:
            return ValidationResult(False, "A mensagem deve ter no máximo 5000 caracteres")
        
        if re.search(cls.DANGEROUS_CONTENT_PATTERN, message, re.I):
            return ValidationResult(False, "A mensagem contém conteúdo não permitido")
        
        return ValidationResult(True)

def log_view_execution(view_func):
    """Decorator to log view execution"""
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing view: {view_func.__name__}")
        try:
            result = view_func(*args, **kwargs)
            logger.info(f"View {view_func.__name__} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in view {view_func.__name__}: {str(e)}")
            raise
    return wrapper

@log_view_execution
def home(request):
    """Render home page"""
    return render(request, 'home.html')

@log_view_execution
def sobre_nos(request):
    """Render about page"""
    return render(request, 'sobre_nos.html')

@log_view_execution
def services(request):
    """Render services page with service data"""
    services_data = [
        {
            'id': 'landing-page',
            'icon': 'bi bi-file-earmark-code',
            'title': 'Landing Page',
            'description': 'Página única e otimizada para conversão de vendas.',
            'features': [
                'Design Responsivo',
                'Otimização SEO Básica',
                'Formulário de Contato',
                'Integração WhatsApp',
                'Hospedagem 6 meses'
            ]
        },
        {
            'id': 'site-institucional',
            'icon': 'bi bi-globe2',
            'title': 'Site Institucional',
            'description': 'Presença digital profissional para sua empresa.',
            'features': [
                'Até 5 Páginas',
                'Design Responsivo',
                'Otimização SEO',
                'Formulário de Contato',
                'Integração WhatsApp',
                'Hospedagem 1 ano'
            ]
        },
        {
            'id': 'site-profissional',
            'icon': 'bi bi-briefcase',
            'title': 'Site Profissional',
            'description': 'Solução completa para pequenas empresas.',
            'features': [
                'Até 8 Páginas',
                'Design Premium',
                'Blog Integrado',
                'SEO Avançado',
                'Área Administrativa',
                'Analytics Integrado',
                'Hospedagem 1 ano',
                'Suporte 6 meses'
            ]
        },
        {
            'id': 'site-empresarial',
            'icon': 'bi bi-building',
            'title': 'Site Empresarial',
            'description': 'Solução robusta para médias empresas com recursos avançados.',
            'features': [
                'Até 15 Páginas',
                'Design Personalizado',
                'Blog Avançado',
                'SEO Premium',
                'Painel Administrativo',
                'Integração ERP',
                'Sistema de Newsletter',
                'Chat Online',
                'Hospedagem 2 anos',
                'Suporte 12 meses'
            ]
        },
        {
            'id': 'loja-virtual',
            'icon': 'bi bi-cart4',
            'title': 'Loja Virtual',
            'description': 'Comece a vender online com uma loja virtual completa.',
            'features': [
                'Produtos Ilimitados',
                'Painel Administrativo',
                'Gestão de Estoque',
                'Múltiplos Pagamentos',
                'Cálculo de Frete',
                'Cupons de Desconto',
                'Relatórios de Vendas',
                'Hospedagem 1 ano'
            ]
        },
        {
            'id': 'suporte-premium',
            'icon': 'bi bi-shield-check',
            'title': 'Premium',
            'description': 'Soluções personalizadas para grandes empresas.',
            'features': [
                'Projeto Personalizado',
                'Consultoria Especializada',
                'Recursos Customizados',
                'Suporte 24/7',
                'SLA Garantido',
                'Hospedagem Premium'
            ]
        }
    ]
    return render(request, 'services.html', {'title': 'Serviços - Hoz Tech', 'services': services_data})

@log_view_execution
def minha_seguranca(request):
    """Render security page"""
    return render(request, 'minha_seguranca.html')

def test_email_sending():
    """Testa o envio de email com dados de teste"""
    print("\n=== Iniciando teste de envio de email ===")
    
    # Dados de teste
    test_data = {
        'name': 'Teste Automático',
        'email': 'test@example.com',
        'phone': '11999999999',
        'subject': 'Teste de Envio',
        'message': 'Este é um email de teste automático enviado em: ' + time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        print("\n1. Testando conexão...")
        connection_ok, connection_msg = test_email_connection()
        if not connection_ok:
            print(f"Falha na conexão: {connection_msg}")
            return False, connection_msg
        
        print("\n2. Preparando email de teste...")
        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Email de Teste Automático</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <p><strong>Nome:</strong> {test_data['name']}</p>
                <p><strong>Email:</strong> {test_data['email']}</p>
                <p><strong>Telefone:</strong> {test_data['phone']}</p>
                <p><strong>Assunto:</strong> {test_data['subject']}</p>
                <div style="margin-top: 20px;">
                    <strong>Mensagem:</strong>
                    <p style="white-space: pre-wrap;">{test_data['message']}</p>
                </div>
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                Este é um email de teste automático do sistema de contato.
            </p>
        </body>
        </html>
        """
        
        print("\n3. Configurações de envio:")
        print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
        print(f"TO: {settings.CONTACT_EMAIL}")
        print(f"SUBJECT: Teste de Envio - {test_data['subject']}")
        
        print("\n4. Tentando enviar email...")
        send_mail(
            subject=f'Teste de Envio - {test_data["subject"]}',
            message=email_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
            html_message=email_content,
        )
        
        print("\n5. Email enviado com sucesso!")
        return True, "Email de teste enviado com sucesso"
        
    except Exception as e:
        print(f"\nERRO no teste: {str(e)}")
        logger.error(f'Falha no teste de envio: {str(e)}', exc_info=True)
        return False, f"Erro no teste: {str(e)}"

def test_email_connection():
    """Testa a conexão com o servidor de email"""
    try:
        print("\n=== Testando conexão com servidor de email ===")
        print(f"Host: {settings.EMAIL_HOST}")
        print(f"Port: {settings.EMAIL_PORT}")
        print(f"TLS: {settings.EMAIL_USE_TLS}")
        print(f"SSL: {settings.EMAIL_USE_SSL}")
        print(f"Username: {settings.EMAIL_HOST_USER}")
        print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
        print(f"Contact Email: {settings.CONTACT_EMAIL}")
        
        connection = get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            use_ssl=settings.EMAIL_USE_SSL,
            timeout=settings.EMAIL_TIMEOUT
        )
        print("\nTentando abrir conexão...")
        connection.open()
        print("Conexão aberta com sucesso!")
        connection.close()
        print("Conexão fechada com sucesso!")
        return True, "Conexão com servidor de email estabelecida com sucesso"
    except Exception as e:
        print(f"\nERRO na conexão: {str(e)}")
        logger.error(f"Erro na conexão com servidor de email: {str(e)}", exc_info=True)
        return False, f"Erro na conexão: {str(e)}"

class ContactFormHandler:
    """Handler class for contact form submissions"""
    
    @staticmethod
    def get_client_ip(request) -> str:
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '0.0.0.0')
    
    @staticmethod
    def check_rate_limit(ip: str) -> bool:
        """Check if IP has exceeded rate limit"""
        cache_key = f'contact_form_{ip}'
        return bool(cache.get(cache_key))
    
    @staticmethod
    def set_rate_limit(ip: str, timeout: int = 300) -> None:
        """Set rate limit for IP"""
        cache_key = f'contact_form_{ip}'
        cache.set(cache_key, True, timeout)
    
    @staticmethod
    def format_email_content(form_data: Dict[str, Any]) -> str:
        """Format email content with HTML"""
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2c3e50;">Nova mensagem de contato</h2>
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px;">
                <p><strong>Nome:</strong> {form_data['name']}</p>
                <p><strong>Email:</strong> {form_data['email']}</p>
                <p><strong>Telefone:</strong> {form_data['phone']}</p>
                <p><strong>Assunto:</strong> {form_data['subject']}</p>
                <div style="margin-top: 20px;">
                    <strong>Mensagem:</strong>
                    <p style="white-space: pre-wrap;">{form_data['message']}</p>
                </div>
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                Esta mensagem foi enviada através do formulário de contato do site Hoz Tech.
            </p>
        </body>
        </html>
        """
    
    @classmethod
    def send_email(cls, form_data: Dict[str, Any]) -> None:
        """Send contact form email"""
        print("\n=== Iniciando envio de email ===")
        print(f"Dados do formulário: {form_data}")
        
        # Testa a conexão antes de enviar
        connection_ok, connection_msg = test_email_connection()
        if not connection_ok:
            print(f"Falha na conexão: {connection_msg}")
            logger.error(f"Falha na conexão com servidor de email: {connection_msg}")
            raise Exception(f"Erro na conexão com servidor de email: {connection_msg}")
        
        email_content = cls.format_email_content(form_data)
        
        try:
            # Log das configurações de email (sem a senha)
            print("\nConfigurações de email:")
            print(f"HOST: {settings.EMAIL_HOST}")
            print(f"PORT: {settings.EMAIL_PORT}")
            print(f"TLS: {settings.EMAIL_USE_TLS}")
            print(f"SSL: {settings.EMAIL_USE_SSL}")
            print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
            print(f"TO: {settings.CONTACT_EMAIL}")
            
            print("\nTentando enviar email...")
            send_mail(
                subject=f'Contato via Site - {form_data["subject"]}',
                message=email_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
                html_message=email_content,
            )
            print("Email enviado com sucesso!")
            logger.info(f'Email enviado com sucesso para {settings.CONTACT_EMAIL}')
        except Exception as e:
            print(f"\nERRO ao enviar email: {str(e)}")
            logger.error(f'Falha ao enviar email: {str(e)}', exc_info=True)
            raise

@require_POST
@csrf_protect
def handle_contact_submission(request):
    """Handle contact form submission"""
    print("\n=== Processando submissão do formulário ===")
    handler = ContactFormHandler()
    client_ip = handler.get_client_ip(request)
    print(f"IP do cliente: {client_ip}")
    
    # Check rate limit
    if handler.check_rate_limit(client_ip):
        print("Rate limit excedido!")
        logger.warning(f'Rate limit exceeded for IP: {client_ip}')
        return JsonResponse({
            'success': False,
            'message': _('Por favor, aguarde alguns minutos antes de enviar outra mensagem.')
        }, status=429)
    
    # Validate form
    print("\nValidando formulário...")
    form = ContactForm(request.POST)
    
    # Remove website from validation if it's empty
    if 'website' in form.data and not form.data['website']:
        form.data = form.data.copy()
        form.data.pop('website')
    
    if not form.is_valid():
        print(f"Erros de validação: {form.errors}")
        errors = {field: form.errors[field][0] for field in form.errors}
        return JsonResponse({
            'success': False,
            'message': _('Por favor, corrija os erros no formulário.'),
            'errors': errors
        }, status=400)
    
    try:
        # Process form data
        print("\nProcessando dados do formulário...")
        form_data = form.get_cleaned_data()
        print(f"Dados processados: {form_data}")
        
        # Send email
        handler.send_email(form_data)
        
        # Set rate limit
        handler.set_rate_limit(client_ip)
        
        print("Formulário processado com sucesso!")
        return JsonResponse({
            'success': True,
            'message': _('Mensagem enviada com sucesso! Entraremos em contato em breve.')
        })
        
    except Exception as e:
        print(f"\nERRO ao processar formulário: {str(e)}")
        logger.error(f'Erro ao processar formulário de contato: {str(e)}', exc_info=True)
        return JsonResponse({
            'success': False,
            'message': _('Erro ao enviar mensagem. Por favor, tente novamente mais tarde.')
        }, status=500)

def contact(request):
    """View para a página de contato"""
    if request.method == 'POST':
        return handle_contact_submission(request)
    
    form = ContactForm()
    return render(request, 'contact.html', {
        'form': form,
        'title': 'Contato',
        'description': 'Entre em contato conosco para mais informações sobre nossos serviços.',
        'email_connection_ok': True  # Removida a execução do teste
    })

@log_view_execution
def privacy(request):
    """Render privacy policy page"""
    return render(request, 'privacy.html')

@log_view_execution
def terms(request):
    """Render terms of service page"""
    return render(request, 'terms.html')

@log_view_execution
def download_pdf(request):
    """Handle PDF download"""
    file_path = os.path.join('media', 'HOZ_TECH.pdf')
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='HOZ_TECH.pdf')
    return render(request, 'home.html', {'error': 'Arquivo não encontrado'})

@method_decorator(staff_member_required, name='dispatch')
class CookieListView(ListView):
    model = Cookie
    template_name = 'admin/cookie_list.html'
    context_object_name = 'cookies'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        domain = self.request.GET.get('domain')
        name = self.request.GET.get('name')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if domain:
            queryset = queryset.filter(domain__icontains=domain)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset.select_related('session')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context['total_cookies'] = queryset.count()
        context['secure_cookies'] = queryset.filter(secure=True).count()
        context['session_cookies'] = queryset.filter(expires__isnull=True).count()
        context['unique_domains'] = queryset.values('domain').distinct().count()
        
        return context

@method_decorator(staff_member_required, name='dispatch')
class SessionListView(ListView):
    model = Session
    template_name = 'admin/visitor_list.html'
    context_object_name = 'sessions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        ip = self.request.GET.get('ip')
        user_agent = self.request.GET.get('user_agent')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if ip:
            queryset = queryset.filter(ip_address__icontains=ip)
        if user_agent:
            queryset = queryset.filter(user_agent__icontains=user_agent)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context['total_visitors'] = queryset.count()
        context['active_visitors'] = queryset.filter(is_active=True).count()
        context['unique_ips'] = queryset.values('ip_address').distinct().count()
        
        # Calculate average session duration
        sessions = queryset.filter(last_activity__isnull=False)
        if sessions.exists():
            total_duration = sum(
                (s.last_activity - s.created_at).total_seconds()
                for s in sessions
            )
            context['avg_session_duration'] = timedelta(seconds=int(total_duration / sessions.count()))
        else:
            context['avg_session_duration'] = timedelta(0)
        
        # Get visitor counts by hour
        today = timezone.now().date()
        visitor_hours = []
        visitor_counts = []
        
        for hour in range(24):
            count = queryset.filter(
                created_at__date=today,
                created_at__hour=hour
            ).count()
            visitor_hours.append(f"{hour:02d}:00")
            visitor_counts.append(count)
        
        context['visitor_hours'] = json.dumps(visitor_hours)
        context['visitor_counts'] = json.dumps(visitor_counts)
        
        # Get browser statistics
        browsers = {}
        for session in queryset:
            browser = session.user_agent.split('/')[0]
            browsers[browser] = browsers.get(browser, 0) + 1
        
        context['browser_names'] = json.dumps(list(browsers.keys()))
        context['browser_counts'] = json.dumps(list(browsers.values()))
        
        return context

@method_decorator(staff_member_required, name='dispatch')
class SEOMetricsListView(ListView):
    model = SEOMetrics
    template_name = 'admin/seo_list.html'
    context_object_name = 'metrics'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        url = self.request.GET.get('url')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if url:
            queryset = queryset.filter(url__icontains=url)
        if date_from:
            queryset = queryset.filter(last_checked__gte=date_from)
        if date_to:
            queryset = queryset.filter(last_checked__lte=date_to)

        return queryset

@method_decorator(staff_member_required, name='dispatch')
class AnalyticsExportListView(ListView):
    model = AnalyticsExport
    template_name = 'admin/export.html'
    context_object_name = 'exports'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

@staff_member_required
def export_cookies(request):
    """Export cookies data"""
    format = request.GET.get('format', 'csv')
    queryset = Cookie.objects.all()
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cookies.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Domain', 'Value', 'Expires', 'Secure', 'HttpOnly', 'SameSite', 'Created At'])
        
        for cookie in queryset:
            writer.writerow([
                cookie.name,
                cookie.domain,
                cookie.value,
                cookie.expires,
                cookie.secure,
                cookie.httponly,
                cookie.samesite,
                cookie.created_at
            ])
        return response
    
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Write headers
        headers = ['Name', 'Domain', 'Value', 'Expires', 'Secure', 'HttpOnly', 'SameSite', 'Created At']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Write data
        for row, cookie in enumerate(queryset, start=1):
            worksheet.write(row, 0, cookie.name)
            worksheet.write(row, 1, cookie.domain)
            worksheet.write(row, 2, cookie.value)
            worksheet.write(row, 3, str(cookie.expires))
            worksheet.write(row, 4, cookie.secure)
            worksheet.write(row, 5, cookie.httponly)
            worksheet.write(row, 6, cookie.samesite)
            worksheet.write(row, 7, str(cookie.created_at))
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="cookies.xlsx"'
        return response
    
    elif format == 'json':
        data = list(queryset.values())
        return JsonResponse(data, safe=False)
    
    return HttpResponse('Invalid format', status=400)

@staff_member_required
def export_sessions(request):
    """Export sessions data"""
    format = request.GET.get('format', 'csv')
    queryset = Session.objects.all()
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sessions.csv"'
        writer = csv.writer(response)
        writer.writerow(['IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'Is Active'])
        
        for session in queryset:
            writer.writerow([
                session.ip_address,
                session.user_agent,
                session.referrer,
                session.created_at,
                session.last_activity,
                session.is_active
            ])
        return response
    
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Write headers
        headers = ['IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'Is Active']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Write data
        for row, session in enumerate(queryset, start=1):
            worksheet.write(row, 0, session.ip_address)
            worksheet.write(row, 1, session.user_agent)
            worksheet.write(row, 2, session.referrer)
            worksheet.write(row, 3, str(session.created_at))
            worksheet.write(row, 4, str(session.last_activity))
            worksheet.write(row, 5, session.is_active)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="sessions.xlsx"'
        return response
    
    elif format == 'json':
        data = list(queryset.values())
        return JsonResponse(data, safe=False)
    
    return HttpResponse('Invalid format', status=400)

@staff_member_required
def export_seo(request):
    """Export SEO metrics data"""
    format = request.GET.get('format', 'csv')
    queryset = SEOMetrics.objects.all()
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="seo_metrics.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'URL', 'Title', 'Meta Description', 'H1 Count', 'H2 Count', 'H3 Count',
            'Image Count', 'Word Count', 'Internal Links', 'External Links',
            'Page Speed Score', 'Mobile Friendly Score', 'Last Checked'
        ])
        
        for metric in queryset:
            writer.writerow([
                metric.url,
                metric.title,
                metric.meta_description,
                metric.h1_count,
                metric.h2_count,
                metric.h3_count,
                metric.image_count,
                metric.word_count,
                metric.internal_links,
                metric.external_links,
                metric.page_speed_score,
                metric.mobile_friendly_score,
                metric.last_checked
            ])
        return response
    
    elif format == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Write headers
        headers = [
            'URL', 'Title', 'Meta Description', 'H1 Count', 'H2 Count', 'H3 Count',
            'Image Count', 'Word Count', 'Internal Links', 'External Links',
            'Page Speed Score', 'Mobile Friendly Score', 'Last Checked'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Write data
        for row, metric in enumerate(queryset, start=1):
            worksheet.write(row, 0, metric.url)
            worksheet.write(row, 1, metric.title)
            worksheet.write(row, 2, metric.meta_description)
            worksheet.write(row, 3, metric.h1_count)
            worksheet.write(row, 4, metric.h2_count)
            worksheet.write(row, 5, metric.h3_count)
            worksheet.write(row, 6, metric.image_count)
            worksheet.write(row, 7, metric.word_count)
            worksheet.write(row, 8, metric.internal_links)
            worksheet.write(row, 9, metric.external_links)
            worksheet.write(row, 10, metric.page_speed_score)
            worksheet.write(row, 11, metric.mobile_friendly_score)
            worksheet.write(row, 12, str(metric.last_checked))
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="seo_metrics.xlsx"'
        return response
    
    elif format == 'json':
        data = list(queryset.values())
        return JsonResponse(data, safe=False)
    
    return HttpResponse('Invalid format', status=400)

@staff_member_required
def export_data(request):
    """Export all analytics data"""
    format = request.GET.get('format', 'csv')
    data_type = request.GET.get('type', 'all')
    
    if data_type == 'cookies':
        return export_cookies(request)
    elif data_type == 'sessions':
        return export_sessions(request)
    elif data_type == 'seo':
        return export_seo(request)
    elif data_type == 'all':
        # Create a zip file containing all exports
        output = BytesIO()
        with zipfile.ZipFile(output, 'w') as zip_file:
            # Export cookies
            cookies_response = export_cookies(request)
            zip_file.writestr('cookies.csv', cookies_response.content)
            
            # Export sessions
            sessions_response = export_sessions(request)
            zip_file.writestr('sessions.csv', sessions_response.content)
            
            # Export SEO metrics
            seo_response = export_seo(request)
            zip_file.writestr('seo_metrics.csv', seo_response.content)
        
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/zip'
        )
        response['Content-Disposition'] = 'attachment; filename="analytics_data.zip"'
        return response
    
    return HttpResponse('Invalid data type', status=400)

@method_decorator(staff_member_required, name='dispatch')
class AdminDashboardView(TemplateView):
    """Admin dashboard view showing overview of all metrics"""
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get counts for the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        context.update({
            'cookie_count': Cookie.objects.filter(created_at__gte=thirty_days_ago).count(),
            'session_count': Session.objects.filter(created_at__gte=thirty_days_ago).count(),
            'pageview_count': PageView.objects.filter(created_at__gte=thirty_days_ago).count(),
            'seo_metrics_count': SEOMetrics.objects.filter(last_checked__gte=thirty_days_ago).count(),
            'recent_cookies': Cookie.objects.order_by('-created_at')[:5],
            'recent_sessions': Session.objects.order_by('-created_at')[:5],
            'recent_pageviews': PageView.objects.order_by('-created_at')[:5],
            'recent_seo_metrics': SEOMetrics.objects.order_by('-last_checked')[:5],
        })
        
        return context 