from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import DatabaseError
import logging

# Configurar logger específico para admin
logger = logging.getLogger('core.admin')

from .models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport

# Configurações do admin site
admin.site.site_header = "HOZ TECH Analytics Admin"
admin.site.site_title = "HOZ TECH Analytics"
admin.site.index_title = "Painel de Controle HOZ TECH Analytics"

def safe_str(obj, default=''):
    """Função segura para converter objetos para string"""
    try:
        return str(obj) if obj else default
    except Exception:
        return default

@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'expires', 'secure', 'httponly', 'samesite', 'created_at', 'is_active')
    list_filter = ('domain', 'secure', 'httponly', 'samesite', 'created_at', 'is_active')
    search_fields = ('name', 'domain', 'value')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    list_per_page = 50

    def get_queryset(self, request):
        try:
            return super().get_queryset(request).select_related('session').filter(is_active=True)
        except DatabaseError as e:
            logger.error(f"Erro no queryset de cookies: {e}")
            return super().get_queryset(request).none()

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Erro ao salvar cookie: {e}")
            raise ValidationError(f"Erro ao salvar cookie: {e}")

    def delete_model(self, request, obj):
        try:
            obj.is_active = False
            obj.save()
        except Exception as e:
            logger.error(f"Erro ao deletar cookie: {e}")
            raise ValidationError(f"Erro ao deletar cookie: {e}")

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'truncated_user_agent', 'truncated_referrer', 'created_at', 'last_activity', 'is_active')
    list_filter = ('is_active', 'created_at', 'last_activity')
    search_fields = ('ip_address', 'user_agent', 'referrer', 'session_key')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('session_key', 'created_at', 'last_activity')
    list_per_page = 50

    def get_queryset(self, request):
        try:
            return super().get_queryset(request).filter(is_active=True)
        except DatabaseError as e:
            logger.error(f"Erro no queryset de sessões: {e}")
            return super().get_queryset(request).none()

    def truncated_user_agent(self, obj):
        try:
            if obj.user_agent:
                return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
            return '-'
        except Exception:
            return '-'
    truncated_user_agent.short_description = 'User Agent'

    def truncated_referrer(self, obj):
        try:
            if obj.referrer:
                return obj.referrer[:50] + '...' if len(obj.referrer) > 50 else obj.referrer
            return '-'
        except Exception:
            return '-'
    truncated_referrer.short_description = 'Referrer'

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Erro ao salvar sessão: {e}")
            raise ValidationError(f"Erro ao salvar sessão: {e}")

    def delete_model(self, request, obj):
        try:
            obj.is_active = False
            obj.save()
        except Exception as e:
            logger.error(f"Erro ao deletar sessão: {e}")
            raise ValidationError(f"Erro ao deletar sessão: {e}")

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('shortened_url', 'title', 'time_spent', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('url', 'title')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('created_at',)
    list_per_page = 50

    def get_queryset(self, request):
        try:
            return super().get_queryset(request).filter(is_active=True)
        except DatabaseError as e:
            logger.error(f"Erro no queryset de pageviews: {e}")
            return super().get_queryset(request).none()

    def shortened_url(self, obj):
        try:
            if obj.url:
                return obj.url[:50] + '...' if len(obj.url) > 50 else obj.url
            return '-'
        except Exception:
            return '-'
    shortened_url.short_description = 'URL'

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Erro ao salvar pageview: {e}")
            raise ValidationError(f"Erro ao salvar pageview: {e}")

    def delete_model(self, request, obj):
        try:
            obj.is_active = False
            obj.save()
        except Exception as e:
            logger.error(f"Erro ao deletar pageview: {e}")
            raise ValidationError(f"Erro ao deletar pageview: {e}")

@admin.register(SEOMetrics)
class SEOMetricsAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'h1_count', 'h2_count', 'h3_count', 'image_count', 'word_count', 'score', 'last_checked', 'is_active')
    list_filter = ('last_checked', 'is_active')
    search_fields = ('url', 'title', 'meta_description')
    date_hierarchy = 'last_checked'
    list_editable = ('is_active',)
    readonly_fields = ('last_checked', 'created_by', 'updated_by')
    list_per_page = 50

    def get_queryset(self, request):
        try:
            return super().get_queryset(request).filter(is_active=True)
        except DatabaseError as e:
            logger.error(f"Erro no queryset de métricas SEO: {e}")
            return super().get_queryset(request).none()

    def score(self, obj):
        try:
            if obj.page_speed_score and obj.mobile_friendly_score:
                return f"{(obj.page_speed_score + obj.mobile_friendly_score) / 2:.1f}"
            return '-'
        except Exception:
            return '-'
    score.short_description = 'Score'

    def save_model(self, request, obj, form, change):
        try:
            if not change:  # Novo objeto
                obj.created_by = request.user
            obj.updated_by = request.user
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Erro ao salvar métrica SEO: {e}")
            raise ValidationError(f"Erro ao salvar métrica SEO: {e}")

    def delete_model(self, request, obj):
        try:
            obj.is_active = False
            obj.save()
        except Exception as e:
            logger.error(f"Erro ao deletar métrica SEO: {e}")
            raise ValidationError(f"Erro ao deletar métrica SEO: {e}")

@admin.register(AnalyticsExport)
class AnalyticsExportAdmin(admin.ModelAdmin):
    list_display = ('name', 'format', 'date_range', 'file_path', 'created_at', 'download_link', 'is_active')
    list_filter = ('format', 'created_at', 'is_active')
    search_fields = ('name', 'file_path')
    date_hierarchy = 'created_at'
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'user')
    list_per_page = 50

    def get_queryset(self, request):
        try:
            return super().get_queryset(request).filter(is_active=True)
        except DatabaseError as e:
            logger.error(f"Erro no queryset de exports: {e}")
            return super().get_queryset(request).none()

    def date_range(self, obj):
        try:
            return f"{obj.date_range_start} to {obj.date_range_end}"
        except Exception:
            return '-'
    date_range.short_description = 'Date Range'

    def download_link(self, obj):
        try:
            if obj.file_path:
                return format_html('<a href="{}" target="_blank">Download</a>', obj.file_path.url)
            return '-'
        except Exception:
            return '-'
    download_link.short_description = 'Download'

    def save_model(self, request, obj, form, change):
        try:
            if not change:  # Novo objeto
                obj.user = request.user
            super().save_model(request, obj, form, change)
        except Exception as e:
            logger.error(f"Erro ao salvar export: {e}")
            raise ValidationError(f"Erro ao salvar export: {e}")

    def delete_model(self, request, obj):
        try:
            obj.is_active = False
            obj.save()
        except Exception as e:
            logger.error(f"Erro ao deletar export: {e}")
            raise ValidationError(f"Erro ao deletar export: {e}")

# Configurações adicionais do admin
admin.site.disable_action('delete_selected')

# Adicionar ações customizadas
@admin.action(description="Desativar itens selecionados")
def deactivate_selected(modeladmin, request, queryset):
    try:
        updated = queryset.update(is_active=False)
        modeladmin.message_user(request, f"{updated} itens foram desativados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao desativar itens: {e}")
        modeladmin.message_user(request, f"Erro ao desativar itens: {e}", level='ERROR')

# Adicionar ações aos modelos
CookieAdmin.actions = [deactivate_selected]
SessionAdmin.actions = [deactivate_selected]
PageViewAdmin.actions = [deactivate_selected]
SEOMetricsAdmin.actions = [deactivate_selected]
AnalyticsExportAdmin.actions = [deactivate_selected] 