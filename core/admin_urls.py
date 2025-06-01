from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'core_admin'

urlpatterns = [
    # Admin dashboard views
    path('', staff_member_required(views.AdminDashboardView.as_view()), name='admin_dashboard'),
    path('cookies/', staff_member_required(views.CookieListView.as_view()), name='cookie_list'),
    path('sessions/', staff_member_required(views.SessionListView.as_view()), name='session_list'),
    path('seo/', staff_member_required(views.SEOMetricsListView.as_view()), name='seometrics_list'),
    path('exports/', staff_member_required(views.AnalyticsExportListView.as_view()), name='analyticsexport_list'),
    
    # Export URLs
    path('export/cookies/', staff_member_required(views.export_cookies), name='export_cookies'),
    path('export/sessions/', staff_member_required(views.export_sessions), name='export_sessions'),
    path('export/seo/', staff_member_required(views.export_seo), name='export_seo'),
    path('export/', staff_member_required(views.export_data), name='export_data'),
]