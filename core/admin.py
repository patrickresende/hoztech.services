from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport

# Configurações do admin site
admin.site.site_header = "HOZ TECH Analytics Admin"
admin.site.site_title = "HOZ TECH Analytics"
admin.site.index_title = "Painel de Controle HOZ TECH Analytics"

@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'expires', 'secure', 'httponly', 'samesite', 'created_at', 'is_active')
    list_filter = ('domain', 'secure', 'httponly', 'samesite', 'created_at', 'is_active')
    search_fields = ('name', 'domain', 'value')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'truncated_user_agent', 'truncated_referrer', 'created_at', 'last_activity', 'is_active')
    list_filter = ('is_active', 'created_at', 'last_activity')
    search_fields = ('ip_address', 'user_agent', 'referrer', 'session_key')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('session_key', 'created_at', 'last_activity')

    def truncated_user_agent(self, obj):
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return '-'
    truncated_user_agent.short_description = 'User Agent'

    def truncated_referrer(self, obj):
        if obj.referrer:
            return obj.referrer[:50] + '...' if len(obj.referrer) > 50 else obj.referrer
        return '-'
    truncated_referrer.short_description = 'Referrer'

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('shortened_url', 'title', 'time_spent', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('url', 'title')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)

    def shortened_url(self, obj):
        if obj.url:
            return obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
        return '-'
    shortened_url.short_description = 'URL'

@admin.register(SEOMetrics)
class SEOMetricsAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'h1_count', 'h2_count', 'h3_count', 'image_count', 'word_count', 'score', 'last_checked', 'is_active')
    list_filter = ('last_checked', 'is_active')
    search_fields = ('url', 'title', 'meta_description')
    date_hierarchy = 'last_checked'
    list_editable = ('is_active',)
    readonly_fields = ('last_checked', 'created_by', 'updated_by')

    def score(self, obj):
        if obj.page_speed_score and obj.mobile_friendly_score:
            return f"{(obj.page_speed_score + obj.mobile_friendly_score) / 2:.1f}"
        return '-'
    score.short_description = 'Score'

@admin.register(AnalyticsExport)
class AnalyticsExportAdmin(admin.ModelAdmin):
    list_display = ('name', 'format', 'date_range', 'file_path', 'created_at', 'download_link', 'is_active')
    list_filter = ('format', 'created_at', 'is_active')
    search_fields = ('name', 'file_path')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'user')

    def date_range(self, obj):
        return f"{obj.date_range_start} to {obj.date_range_end}"
    date_range.short_description = 'Date Range'

    def download_link(self, obj):
        if obj.file_path:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.file_path.url)
        return '-'
    download_link.short_description = 'Download' 