from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, connection
import csv
import json
import logging
from io import BytesIO
import traceback

# Configurar logger específico para admin
logger = logging.getLogger('core.admin')

# Importações condicionais para evitar erros em produção
try:
    import xlsxwriter
    XLSXWRITER_AVAILABLE = True
except ImportError:
    XLSXWRITER_AVAILABLE = False
    logger.warning("XlsxWriter não está disponível. Exportação Excel será desabilitada.")

from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport

def safe_count(queryset):
    """Conta segura de objetos com tratamento de erro"""
    try:
        return queryset.count()
    except (DatabaseError, Exception) as e:
        logger.error(f"Erro ao contar objetos: {e}")
        return 0

def safe_queryset(queryset, limit=None):
    """Executa queryset de forma segura com limite opcional"""
    try:
        if limit:
            return list(queryset[:limit])
        return list(queryset)
    except (DatabaseError, Exception) as e:
        logger.error(f"Erro ao executar queryset: {e}")
        return []

@staff_member_required
def admin_dashboard(request):
    """Dashboard principal do admin com tratamento robusto de erros"""
    try:
        # Estatísticas gerais com tratamento de erro
        total_sessions = safe_count(Session.objects.filter(is_active=True))
        total_pageviews = safe_count(PageView.objects.filter(is_active=True))
        total_cookies = safe_count(Cookie.objects.filter(is_active=True))
        total_seo_metrics = safe_count(SEOMetrics.objects.filter(is_active=True))

        # Sessões ativas nas últimas 24 horas
        last_24h = timezone.now() - timedelta(hours=24)
        active_sessions = safe_count(
            Session.objects.filter(
                last_activity__gte=last_24h,
                is_active=True
            )
        )

        # Top páginas visitadas (limitado para performance)
        top_pages = safe_queryset(
            PageView.objects.filter(is_active=True).values(
                'url', 'title'
            ).annotate(
                total=Count('id')
            ).order_by('-total')[:5]
        )

        # Métricas SEO (limitado para performance)
        seo_metrics = safe_queryset(
            SEOMetrics.objects.filter(is_active=True).order_by('-page_speed_score')[:5]
        )

        # Dados para JavaScript
        dashboard_data = {
            'totalSessions': total_sessions,
            'totalPageviews': total_pageviews,
            'totalCookies': total_cookies,
            'totalSeoMetrics': total_seo_metrics,
            'activeSessions': active_sessions,
            'exportUrl': '/core_admin/export/data/',
            'xlsxAvailable': XLSXWRITER_AVAILABLE
        }

        context = {
            'total_sessions': total_sessions,
            'total_pageviews': total_pageviews,
            'total_cookies': total_cookies,
            'total_seo_metrics': total_seo_metrics,
            'active_sessions': active_sessions,
            'top_pages': top_pages,
            'seo_metrics': seo_metrics,
            'dashboard_data': json.dumps(dashboard_data),
            'title': 'Dashboard',
            'xlsx_available': XLSXWRITER_AVAILABLE,
        }

        return render(request, 'admin/dashboard.html', context)

    except Exception as e:
        logger.error(f"Erro no dashboard admin: {e}")
        logger.error(traceback.format_exc())
        
        # Contexto de fallback
        fallback_context = {
            'error_message': 'Erro ao carregar dashboard. Tente novamente.',
            'title': 'Dashboard - Erro',
            'total_sessions': 0,
            'total_pageviews': 0,
            'total_cookies': 0,
            'total_seo_metrics': 0,
            'active_sessions': 0,
            'top_pages': [],
            'seo_metrics': [],
            'dashboard_data': json.dumps({}),
            'xlsx_available': XLSXWRITER_AVAILABLE,
        }
        
        return render(request, 'admin/dashboard.html', fallback_context, status=500)

@staff_member_required
def cookie_list(request):
    """Lista de cookies com paginação e tratamento de erro"""
    try:
        cookies = safe_queryset(
            Cookie.objects.filter(is_active=True).select_related('session')[:100]
        )
        return render(request, 'admin/cookie_list.html', {
            'cookies': cookies, 
            'title': 'Cookies',
            'total_count': len(cookies)
        })
    except Exception as e:
        logger.error(f"Erro na lista de cookies: {e}")
        return render(request, 'admin/cookie_list.html', {
            'cookies': [], 
            'title': 'Cookies - Erro',
            'error_message': 'Erro ao carregar cookies.',
            'total_count': 0
        }, status=500)

@staff_member_required
def session_list(request):
    """Lista de sessões com tratamento de erro"""
    try:
        sessions = safe_queryset(
            Session.objects.filter(is_active=True).order_by('-last_activity')[:100]
        )
        return render(request, 'admin/session_list_simple.html', {
            'sessions': sessions, 
            'title': 'Sessões',
            'total_count': len(sessions)
        })
    except Exception as e:
        logger.error(f"Erro na lista de sessões: {e}")
        return render(request, 'admin/session_list_simple.html', {
            'sessions': [], 
            'title': 'Sessões - Erro',
            'error_message': 'Erro ao carregar sessões.',
            'total_count': 0
        }, status=500)

@staff_member_required
def seometrics_list(request):
    """Lista de métricas SEO com tratamento de erro"""
    try:
        metrics = safe_queryset(
            SEOMetrics.objects.filter(is_active=True).order_by('-last_checked')[:100]
        )
        return render(request, 'admin/seometrics_list_simple.html', {
            'metrics': metrics, 
            'title': 'SEO Metrics',
            'total_count': len(metrics)
        })
    except Exception as e:
        logger.error(f"Erro na lista de métricas SEO: {e}")
        return render(request, 'admin/seometrics_list_simple.html', {
            'metrics': [], 
            'title': 'SEO Metrics - Erro',
            'error_message': 'Erro ao carregar métricas SEO.',
            'total_count': 0
        }, status=500)

@staff_member_required
def analyticsexport_list(request):
    """Lista de exports com tratamento de erro"""
    try:
        exports = safe_queryset(
            AnalyticsExport.objects.filter(is_active=True).order_by('-created_at')[:50]
        )
        return render(request, 'admin/analyticsexport_list_simple.html', {
            'exports': exports, 
            'title': 'Analytics Export',
            'total_count': len(exports)
        })
    except Exception as e:
        logger.error(f"Erro na lista de exports: {e}")
        return render(request, 'admin/analyticsexport_list_simple.html', {
            'exports': [], 
            'title': 'Analytics Export - Erro',
            'error_message': 'Erro ao carregar exports.',
            'total_count': 0
        }, status=500)

# Funções de Export com tratamento robusto de erros
@staff_member_required
def export_cookies(request):
    """Export cookies data to CSV with error handling"""
    try:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="cookies_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Domain', 'Path', 'Secure', 'HttpOnly', 'SameSite', 'Created At', 'Session IP'])
        
        cookies = safe_queryset(
            Cookie.objects.filter(is_active=True).select_related('session')
        )
        
        for cookie in cookies:
            try:
                writer.writerow([
                    cookie.name or '',
                    cookie.domain or '',
                    cookie.path or '',
                    'Yes' if cookie.secure else 'No',
                    'Yes' if cookie.httponly else 'No',
                    cookie.samesite or 'N/A',
                    cookie.created_at.strftime('%Y-%m-%d %H:%M:%S') if cookie.created_at else 'N/A',
                    cookie.session.ip_address if cookie.session else 'N/A'
                ])
            except Exception as e:
                logger.warning(f"Erro ao processar cookie {cookie.id}: {e}")
                continue
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no export de cookies: {e}")
        return HttpResponse("Erro ao exportar cookies", status=500)

@staff_member_required
def export_sessions(request):
    """Export sessions data to CSV with error handling"""
    try:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="sessions_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Session Key', 'IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'User'])
        
        sessions = safe_queryset(
            Session.objects.filter(is_active=True).select_related('user')
        )
        
        for session in sessions:
            try:
                writer.writerow([
                    session.session_key or '',
                    session.ip_address or '',
                    (session.user_agent[:100] if session.user_agent else '') or '',
                    session.referrer or 'N/A',
                    session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else 'N/A',
                    session.last_activity.strftime('%Y-%m-%d %H:%M:%S') if session.last_activity else 'N/A',
                    session.user.username if session.user else 'Anonymous'
                ])
            except Exception as e:
                logger.warning(f"Erro ao processar sessão {session.id}: {e}")
                continue
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no export de sessões: {e}")
        return HttpResponse("Erro ao exportar sessões", status=500)

@staff_member_required
def export_seo(request):
    """Export SEO metrics data to CSV with error handling"""
    try:
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="seo_metrics_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'URL', 'Title', 'H1 Count', 'H2 Count', 'H3 Count', 'Image Count', 
            'Word Count', 'Internal Links', 'External Links', 'Page Speed Score', 
            'Mobile Friendly Score', 'Last Checked'
        ])
        
        metrics = safe_queryset(SEOMetrics.objects.filter(is_active=True))
        
        for metric in metrics:
            try:
                writer.writerow([
                    metric.url or '',
                    metric.title or '',
                    metric.h1_count or 0,
                    metric.h2_count or 0,
                    metric.h3_count or 0,
                    metric.image_count or 0,
                    metric.word_count or 0,
                    metric.internal_links or 0,
                    metric.external_links or 0,
                    metric.page_speed_score or 'N/A',
                    metric.mobile_friendly_score or 'N/A',
                    metric.last_checked.strftime('%Y-%m-%d %H:%M:%S') if metric.last_checked else 'N/A'
                ])
            except Exception as e:
                logger.warning(f"Erro ao processar métrica SEO {metric.id}: {e}")
                continue
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no export de métricas SEO: {e}")
        return HttpResponse("Erro ao exportar métricas SEO", status=500)

@staff_member_required
def export_data(request):
    """Export all data to Excel file with error handling"""
    if not XLSXWRITER_AVAILABLE:
        return HttpResponse("Exportação Excel não disponível. XlsxWriter não está instalado.", status=503)
    
    try:
        # Create Excel file in memory
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })
        
        # Cookies sheet
        cookies_worksheet = workbook.add_worksheet('Cookies')
        cookies_headers = ['Name', 'Domain', 'Path', 'Secure', 'HttpOnly', 'SameSite', 'Created At', 'Session IP']
        
        for col, header in enumerate(cookies_headers):
            cookies_worksheet.write(0, col, header, header_format)
        
        cookies = safe_queryset(
            Cookie.objects.filter(is_active=True).select_related('session')
        )
        
        for row, cookie in enumerate(cookies, 1):
            try:
                cookies_worksheet.write(row, 0, cookie.name or '')
                cookies_worksheet.write(row, 1, cookie.domain or '')
                cookies_worksheet.write(row, 2, cookie.path or '')
                cookies_worksheet.write(row, 3, 'Yes' if cookie.secure else 'No')
                cookies_worksheet.write(row, 4, 'Yes' if cookie.httponly else 'No')
                cookies_worksheet.write(row, 5, cookie.samesite or 'N/A')
                cookies_worksheet.write(row, 6, cookie.created_at.strftime('%Y-%m-%d %H:%M:%S') if cookie.created_at else 'N/A')
                cookies_worksheet.write(row, 7, cookie.session.ip_address if cookie.session else 'N/A')
            except Exception as e:
                logger.warning(f"Erro ao processar cookie {cookie.id} no Excel: {e}")
                continue
        
        # Sessions sheet
        sessions_worksheet = workbook.add_worksheet('Sessions')
        sessions_headers = ['Session Key', 'IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'User']
        
        for col, header in enumerate(sessions_headers):
            sessions_worksheet.write(0, col, header, header_format)
        
        sessions = safe_queryset(
            Session.objects.filter(is_active=True).select_related('user')
        )
        
        for row, session in enumerate(sessions, 1):
            try:
                sessions_worksheet.write(row, 0, session.session_key or '')
                sessions_worksheet.write(row, 1, session.ip_address or '')
                sessions_worksheet.write(row, 2, session.user_agent[:100] if session.user_agent else '')
                sessions_worksheet.write(row, 3, session.referrer or 'N/A')
                sessions_worksheet.write(row, 4, session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else 'N/A')
                sessions_worksheet.write(row, 5, session.last_activity.strftime('%Y-%m-%d %H:%M:%S') if session.last_activity else 'N/A')
                sessions_worksheet.write(row, 6, session.user.username if session.user else 'Anonymous')
            except Exception as e:
                logger.warning(f"Erro ao processar sessão {session.id} no Excel: {e}")
                continue
        
        # SEO Metrics sheet
        seo_worksheet = workbook.add_worksheet('SEO Metrics')
        seo_headers = [
            'URL', 'Title', 'H1 Count', 'H2 Count', 'H3 Count', 'Image Count', 
            'Word Count', 'Internal Links', 'External Links', 'Page Speed Score', 
            'Mobile Friendly Score', 'Last Checked'
        ]
        
        for col, header in enumerate(seo_headers):
            seo_worksheet.write(0, col, header, header_format)
        
        metrics = safe_queryset(SEOMetrics.objects.filter(is_active=True))
        
        for row, metric in enumerate(metrics, 1):
            try:
                seo_worksheet.write(row, 0, metric.url or '')
                seo_worksheet.write(row, 1, metric.title or '')
                seo_worksheet.write(row, 2, metric.h1_count or 0)
                seo_worksheet.write(row, 3, metric.h2_count or 0)
                seo_worksheet.write(row, 4, metric.h3_count or 0)
                seo_worksheet.write(row, 5, metric.image_count or 0)
                seo_worksheet.write(row, 6, metric.word_count or 0)
                seo_worksheet.write(row, 7, metric.internal_links or 0)
                seo_worksheet.write(row, 8, metric.external_links or 0)
                seo_worksheet.write(row, 9, metric.page_speed_score or 'N/A')
                seo_worksheet.write(row, 10, metric.mobile_friendly_score or 'N/A')
                seo_worksheet.write(row, 11, metric.last_checked.strftime('%Y-%m-%d %H:%M:%S') if metric.last_checked else 'N/A')
            except Exception as e:
                logger.warning(f"Erro ao processar métrica SEO {metric.id} no Excel: {e}")
                continue
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="analytics_export.xlsx"'
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no export Excel: {e}")
        logger.error(traceback.format_exc())
        return HttpResponse("Erro ao gerar arquivo Excel", status=500)

@staff_member_required
def test_view(request):
    """View de teste simples com tratamento de erro"""
    try:
        sessions = safe_queryset(Session.objects.filter(is_active=True)[:5])
        exports = safe_queryset(AnalyticsExport.objects.filter(is_active=True)[:5])
        metrics = safe_queryset(SEOMetrics.objects.filter(is_active=True)[:5])
        
        context = {
            'sessions': sessions,
            'exports': exports,
            'metrics': metrics,
            'title': 'Test View',
            'test_data': 'Dados de teste funcionando!',
            'xlsx_available': XLSXWRITER_AVAILABLE,
            'database_connection': 'OK' if connection.ensure_connection() else 'ERRO'
        }
        
        return render(request, 'admin/test_view.html', context)
        
    except Exception as e:
        logger.error(f"Erro na view de teste: {e}")
        return render(request, 'admin/test_view.html', {
            'sessions': [],
            'exports': [],
            'metrics': [],
            'title': 'Test View - Erro',
            'test_data': f'Erro: {str(e)}',
            'xlsx_available': XLSXWRITER_AVAILABLE,
            'database_connection': 'ERRO',
            'error_message': 'Erro ao carregar dados de teste.'
        }, status=500) 