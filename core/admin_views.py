from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
from django.http import HttpResponse
import csv
import xlsxwriter
from io import BytesIO
import json
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect

@staff_member_required
def admin_dashboard(request):
    # Estatísticas gerais
    total_sessions = Session.objects.count()
    total_pageviews = PageView.objects.count()
    total_cookies = Cookie.objects.count()
    total_seo_metrics = SEOMetrics.objects.count()

    # Sessões ativas nas últimas 24 horas
    last_24h = timezone.now() - timedelta(hours=24)
    active_sessions = Session.objects.filter(
        last_activity__gte=last_24h
    ).count()

    # Top páginas visitadas
    top_pages = PageView.objects.values(
        'url', 'title'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    # Métricas SEO
    seo_metrics = SEOMetrics.objects.order_by('-page_speed_score')[:5]

    context = {
        'total_sessions': total_sessions,
        'total_pageviews': total_pageviews,
        'total_cookies': total_cookies,
        'total_seo_metrics': total_seo_metrics,
        'active_sessions': active_sessions,
        'top_pages': top_pages,
        'seo_metrics': seo_metrics,
        'title': 'Dashboard',
    }

    return render(request, 'admin/dashboard.html', context)

@staff_member_required
def cookie_list(request):
    cookies = Cookie.objects.all().select_related('session')
    return render(request, 'admin/cookie_list.html', {'cookies': cookies, 'title': 'Cookies'})

@staff_member_required
def session_list(request):
    sessions = Session.objects.all().order_by('-last_activity')
    return render(request, 'admin/session_list_simple.html', {'sessions': sessions, 'title': 'Sessões'})

@staff_member_required
def seometrics_list(request):
    metrics = SEOMetrics.objects.all().order_by('-last_checked')
    return render(request, 'admin/seometrics_list_simple.html', {'metrics': metrics, 'title': 'SEO Metrics'})

@staff_member_required
def analyticsexport_list(request):
    exports = AnalyticsExport.objects.all().order_by('-created_at')
    return render(request, 'admin/analyticsexport_list_simple.html', {'exports': exports, 'title': 'Analytics Export'})

# Funções de Export
@staff_member_required
def export_cookies(request):
    """Export cookies data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cookies_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Domain', 'Path', 'Secure', 'HttpOnly', 'SameSite', 'Created At', 'Session IP'])
    
    cookies = Cookie.objects.all().select_related('session')
    for cookie in cookies:
        writer.writerow([
            cookie.name,
            cookie.domain,
            cookie.path,
            cookie.secure,
            cookie.httponly,
            cookie.samesite,
            cookie.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            cookie.session.ip_address if cookie.session else 'N/A'
        ])
    
    return response

@staff_member_required
def export_sessions(request):
    """Export sessions data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sessions_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Session Key', 'IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'User'])
    
    sessions = Session.objects.all().select_related('user')
    for session in sessions:
        writer.writerow([
            session.session_key,
            session.ip_address,
            session.user_agent[:100],  # Truncate long user agents
            session.referrer or 'N/A',
            session.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            session.last_activity.strftime('%Y-%m-%d %H:%M:%S'),
            session.user.username if session.user else 'Anonymous'
        ])
    
    return response

@staff_member_required
def export_seo(request):
    """Export SEO metrics data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="seo_metrics_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'URL', 'Title', 'H1 Count', 'H2 Count', 'H3 Count', 'Image Count', 
        'Word Count', 'Internal Links', 'External Links', 'Page Speed Score', 
        'Mobile Friendly Score', 'Last Checked'
    ])
    
    metrics = SEOMetrics.objects.all()
    for metric in metrics:
        writer.writerow([
            metric.url,
            metric.title,
            metric.h1_count,
            metric.h2_count,
            metric.h3_count,
            metric.image_count,
            metric.word_count,
            metric.internal_links,
            metric.external_links,
            metric.page_speed_score or 'N/A',
            metric.mobile_friendly_score or 'N/A',
            metric.last_checked.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@staff_member_required
def export_data(request):
    """Export all data to Excel file"""
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
    
    cookies = Cookie.objects.all().select_related('session')
    for row, cookie in enumerate(cookies, 1):
        cookies_worksheet.write(row, 0, cookie.name)
        cookies_worksheet.write(row, 1, cookie.domain)
        cookies_worksheet.write(row, 2, cookie.path)
        cookies_worksheet.write(row, 3, 'Yes' if cookie.secure else 'No')
        cookies_worksheet.write(row, 4, 'Yes' if cookie.httponly else 'No')
        cookies_worksheet.write(row, 5, cookie.samesite or 'N/A')
        cookies_worksheet.write(row, 6, cookie.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        cookies_worksheet.write(row, 7, cookie.session.ip_address if cookie.session else 'N/A')
    
    # Sessions sheet
    sessions_worksheet = workbook.add_worksheet('Sessions')
    sessions_headers = ['Session Key', 'IP Address', 'User Agent', 'Referrer', 'Created At', 'Last Activity', 'User']
    
    for col, header in enumerate(sessions_headers):
        sessions_worksheet.write(0, col, header, header_format)
    
    sessions = Session.objects.all().select_related('user')
    for row, session in enumerate(sessions, 1):
        sessions_worksheet.write(row, 0, session.session_key)
        sessions_worksheet.write(row, 1, session.ip_address)
        sessions_worksheet.write(row, 2, session.user_agent[:100])
        sessions_worksheet.write(row, 3, session.referrer or 'N/A')
        sessions_worksheet.write(row, 4, session.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        sessions_worksheet.write(row, 5, session.last_activity.strftime('%Y-%m-%d %H:%M:%S'))
        sessions_worksheet.write(row, 6, session.user.username if session.user else 'Anonymous')
    
    # SEO Metrics sheet
    seo_worksheet = workbook.add_worksheet('SEO Metrics')
    seo_headers = [
        'URL', 'Title', 'H1 Count', 'H2 Count', 'H3 Count', 'Image Count', 
        'Word Count', 'Internal Links', 'External Links', 'Page Speed Score', 
        'Mobile Friendly Score', 'Last Checked'
    ]
    
    for col, header in enumerate(seo_headers):
        seo_worksheet.write(0, col, header, header_format)
    
    metrics = SEOMetrics.objects.all()
    for row, metric in enumerate(metrics, 1):
        seo_worksheet.write(row, 0, metric.url)
        seo_worksheet.write(row, 1, metric.title)
        seo_worksheet.write(row, 2, metric.h1_count)
        seo_worksheet.write(row, 3, metric.h2_count)
        seo_worksheet.write(row, 4, metric.h3_count)
        seo_worksheet.write(row, 5, metric.image_count)
        seo_worksheet.write(row, 6, metric.word_count)
        seo_worksheet.write(row, 7, metric.internal_links)
        seo_worksheet.write(row, 8, metric.external_links)
        seo_worksheet.write(row, 9, metric.page_speed_score or 'N/A')
        seo_worksheet.write(row, 10, metric.mobile_friendly_score or 'N/A')
        seo_worksheet.write(row, 11, metric.last_checked.strftime('%Y-%m-%d %H:%M:%S'))
    
    workbook.close()
    output.seek(0)
    
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="analytics_export.xlsx"'
    
    return response 

@staff_member_required
def test_view(request):
    """View de teste simples"""
    sessions = Session.objects.all()[:5]
    exports = AnalyticsExport.objects.all()[:5]
    metrics = SEOMetrics.objects.all()[:5]
    
    context = {
        'sessions': sessions,
        'exports': exports,
        'metrics': metrics,
        'title': 'Test View',
        'test_data': 'Dados de teste funcionando!'
    }
    
    return render(request, 'admin/test_view.html', context)

# Funções de Limpeza de Dados
@staff_member_required
def clear_data_period(request):
    """Limpar dados por período"""
    
    period = request.POST.get('period', 'hour')
    success = False
    deleted_count = 0
    
    try:
        now = timezone.now()
        
        if period == 'hour':
            # Última hora
            cutoff_time = now - timedelta(hours=1)
            deleted_count = clear_data_since(cutoff_time)
        elif period == 'day':
            # Último dia
            cutoff_time = now - timedelta(days=1)
            deleted_count = clear_data_since(cutoff_time)
        elif period == 'week':
            # Última semana
            cutoff_time = now - timedelta(weeks=1)
            deleted_count = clear_data_since(cutoff_time)
        elif period == 'month':
            # Último mês
            cutoff_time = now - timedelta(days=30)
            deleted_count = clear_data_since(cutoff_time)
        elif period == 'all':
            # Todos os dados
            deleted_count = clear_all_data()
        
        success = True
        
    except Exception as e:
        success = False
        error_message = str(e)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Requisição AJAX
        return JsonResponse({
            'success': success,
            'deleted_count': deleted_count,
            'period': period,
            'message': f'Dados limpos com sucesso! {deleted_count} registros removidos.' if success else f'Erro: {error_message}'
        })
    else:
        # Requisição normal - redirecionar
        if success:
            messages.success(request, f'Dados limpos com sucesso! {deleted_count} registros removidos.')
        else:
            messages.error(request, f'Erro ao limpar dados: {error_message}')
        
        return redirect('core_admin:admin_dashboard')

def clear_data_since(cutoff_time):
    """Limpar dados desde uma data específica"""
    deleted_count = 0
    
    # Limpar PageViews
    pageviews_deleted = PageView.objects.filter(created_at__lt=cutoff_time).count()
    PageView.objects.filter(created_at__lt=cutoff_time).delete()
    deleted_count += pageviews_deleted
    
    # Limpar Cookies
    cookies_deleted = Cookie.objects.filter(created_at__lt=cutoff_time).count()
    Cookie.objects.filter(created_at__lt=cutoff_time).delete()
    deleted_count += cookies_deleted
    
    # Limpar Sessões (apenas as que não têm mais PageViews)
    sessions_to_delete = Session.objects.filter(
        created_at__lt=cutoff_time,
        page_views__isnull=True
    )
    sessions_deleted = sessions_to_delete.count()
    sessions_to_delete.delete()
    deleted_count += sessions_deleted
    
    # Limpar Analytics Exports
    exports_deleted = AnalyticsExport.objects.filter(created_at__lt=cutoff_time).count()
    AnalyticsExport.objects.filter(created_at__lt=cutoff_time).delete()
    deleted_count += exports_deleted
    
    return deleted_count

def clear_all_data():
    """Limpar todos os dados"""
    deleted_count = 0
    
    # Limpar todos os dados em ordem para evitar problemas de foreign key
    pageviews_deleted = PageView.objects.count()
    PageView.objects.all().delete()
    deleted_count += pageviews_deleted
    
    cookies_deleted = Cookie.objects.count()
    Cookie.objects.all().delete()
    deleted_count += cookies_deleted
    
    sessions_deleted = Session.objects.count()
    Session.objects.all().delete()
    deleted_count += sessions_deleted
    
    exports_deleted = AnalyticsExport.objects.count()
    AnalyticsExport.objects.all().delete()
    deleted_count += exports_deleted
    
    # Não limpar SEOMetrics pois são dados importantes para análise
    # seo_deleted = SEOMetrics.objects.count()
    # SEOMetrics.objects.all().delete()
    # deleted_count += seo_deleted
    
    return deleted_count

@staff_member_required
def get_data_stats(request):
    """Obter estatísticas dos dados para o dashboard"""
    
    try:
        # Estatísticas gerais
        total_sessions = Session.objects.count()
        total_pageviews = PageView.objects.count()
        total_cookies = Cookie.objects.count()
        total_seo_metrics = SEOMetrics.objects.count()
        total_exports = AnalyticsExport.objects.count()
        
        # Sessões ativas nas últimas 24 horas
        last_24h = timezone.now() - timedelta(hours=24)
        active_sessions = Session.objects.filter(
            last_activity__gte=last_24h
        ).count()
        
        # Dados por período
        now = timezone.now()
        periods = {
            'hour': now - timedelta(hours=1),
            'day': now - timedelta(days=1),
            'week': now - timedelta(weeks=1),
            'month': now - timedelta(days=30)
        }
        
        period_stats = {}
        for period_name, cutoff_time in periods.items():
            period_stats[period_name] = {
                'sessions': Session.objects.filter(created_at__gte=cutoff_time).count(),
                'pageviews': PageView.objects.filter(created_at__gte=cutoff_time).count(),
                'cookies': Cookie.objects.filter(created_at__gte=cutoff_time).count(),
                'exports': AnalyticsExport.objects.filter(created_at__gte=cutoff_time).count()
            }
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_sessions': total_sessions,
                'total_pageviews': total_pageviews,
                'total_cookies': total_cookies,
                'total_seo_metrics': total_seo_metrics,
                'total_exports': total_exports,
                'active_sessions': active_sessions,
                'period_stats': period_stats
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }) 