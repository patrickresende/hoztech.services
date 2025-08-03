from django.urls import path
from . import admin_views
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'core_admin'

urlpatterns = [
    # Admin dashboard views
    path('', staff_member_required(admin_views.admin_dashboard), name='admin_dashboard'),
    path('cookies/', staff_member_required(admin_views.cookie_list), name='cookie_list'),
    path('sessions/', staff_member_required(admin_views.session_list), name='session_list'),
    path('seo/', staff_member_required(admin_views.seometrics_list), name='seometrics_list'),
    path('exports/', staff_member_required(admin_views.analyticsexport_list), name='analyticsexport_list'),
    path('test/', staff_member_required(admin_views.test_view), name='test_view'),
    
    # Export URLs
    path('export/cookies/', staff_member_required(admin_views.export_cookies), name='export_cookies'),
    path('export/sessions/', staff_member_required(admin_views.export_sessions), name='export_sessions'),
    path('export/seo/', staff_member_required(admin_views.export_seo), name='export_seo'),
    path('export/', staff_member_required(admin_views.export_data), name='export_data'),
    
    # Data management URLs
    path('clear-data/', staff_member_required(admin_views.clear_data_period), name='clear_data_period'),
    path('get-stats/', staff_member_required(admin_views.get_data_stats), name='get_data_stats'),
]