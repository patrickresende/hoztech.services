from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport

@staff_member_required
def admin_dashboard(request):
    # Estatísticas gerais
    total_sessions = Session.objects.filter(is_active=True).count()
    total_pageviews = PageView.objects.filter(is_active=True).count()
    total_cookies = Cookie.objects.filter(is_active=True).count()
    total_seo_metrics = SEOMetrics.objects.filter(is_active=True).count()

    # Sessões ativas nas últimas 24 horas
    last_24h = timezone.now() - timedelta(hours=24)
    active_sessions = Session.objects.filter(
        last_activity__gte=last_24h,
        is_active=True
    ).count()

    # Top páginas visitadas
    top_pages = PageView.objects.filter(is_active=True).values(
        'url', 'title'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    # Métricas SEO
    seo_metrics = SEOMetrics.objects.filter(
        is_active=True
    ).order_by('-page_speed_score')[:5]

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
    cookies = Cookie.objects.filter(is_active=True).select_related('session')
    return render(request, 'admin/cookie_list.html', {'cookies': cookies, 'title': 'Cookies'})

@staff_member_required
def session_list(request):
    sessions = Session.objects.filter(is_active=True)
    return render(request, 'admin/session_list.html', {'sessions': sessions, 'title': 'Sessões'})

@staff_member_required
def seometrics_list(request):
    metrics = SEOMetrics.objects.filter(is_active=True)
    return render(request, 'admin/seometrics_list.html', {'metrics': metrics, 'title': 'SEO Metrics'})

@staff_member_required
def analyticsexport_list(request):
    exports = AnalyticsExport.objects.filter(is_active=True)
    return render(request, 'admin/analyticsexport_list.html', {'exports': exports, 'title': 'Analytics Export'}) 