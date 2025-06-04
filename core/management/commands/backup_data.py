from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Cookie, Session, PageView, SEOMetrics, AnalyticsExport
import json
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup ou restauração dos dados de tráfego do site'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            choices=['backup', 'restore'],
            default='backup',
            help='Ação a ser executada: backup ou restore'
        )
        parser.add_argument(
            '--file',
            type=str,
            help='Arquivo para backup/restore (opcional)'
        )

    def handle(self, *args, **options):
        action = options['action']
        file_path = options.get('file')

        if not file_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = f'backup_data_{timestamp}.json'

        if action == 'backup':
            self.backup_data(file_path)
        else:
            self.restore_data(file_path)

    def backup_data(self, file_path):
        """Realiza o backup dos dados"""
        data = {
            'cookies': [],
            'sessions': [],
            'pageviews': [],
            'seo_metrics': [],
            'analytics_exports': []
        }

        # Backup de Sessões
        self.stdout.write('Fazendo backup das sessões...')
        for session in Session.objects.filter(is_active=True):
            session_data = {
                'session_key': session.session_key,
                'ip_address': session.ip_address,
                'user_agent': session.user_agent,
                'referrer': session.referrer,
                'created_at': session.created_at.isoformat(),
                'last_activity': session.last_activity.isoformat(),
                'is_active': session.is_active
            }
            data['sessions'].append(session_data)

        # Backup de Cookies
        self.stdout.write('Fazendo backup dos cookies...')
        for cookie in Cookie.objects.filter(is_active=True):
            cookie_data = {
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires.isoformat() if cookie.expires else None,
                'secure': cookie.secure,
                'httponly': cookie.httponly,
                'samesite': cookie.samesite,
                'created_at': cookie.created_at.isoformat(),
                'updated_at': cookie.updated_at.isoformat(),
                'session_key': cookie.session.session_key,
                'is_active': cookie.is_active
            }
            data['cookies'].append(cookie_data)

        # Backup de PageViews
        self.stdout.write('Fazendo backup das visualizações de página...')
        for pageview in PageView.objects.filter(is_active=True):
            pageview_data = {
                'session_key': pageview.session.session_key,
                'url': pageview.url,
                'title': pageview.title,
                'time_spent': str(pageview.time_spent) if pageview.time_spent else None,
                'created_at': pageview.created_at.isoformat(),
                'is_active': pageview.is_active
            }
            data['pageviews'].append(pageview_data)

        # Backup de SEO Metrics
        self.stdout.write('Fazendo backup das métricas SEO...')
        for metric in SEOMetrics.objects.filter(is_active=True):
            metric_data = {
                'url': metric.url,
                'title': metric.title,
                'meta_description': metric.meta_description,
                'h1_count': metric.h1_count,
                'h2_count': metric.h2_count,
                'h3_count': metric.h3_count,
                'image_count': metric.image_count,
                'word_count': metric.word_count,
                'internal_links': metric.internal_links,
                'external_links': metric.external_links,
                'last_checked': metric.last_checked.isoformat(),
                'page_speed_score': metric.page_speed_score,
                'mobile_friendly_score': metric.mobile_friendly_score,
                'is_active': metric.is_active
            }
            data['seo_metrics'].append(metric_data)

        # Backup de Analytics Exports
        self.stdout.write('Fazendo backup dos exports de analytics...')
        for export in AnalyticsExport.objects.filter(is_active=True):
            export_data = {
                'name': export.name,
                'format': export.format,
                'date_range_start': export.date_range_start.isoformat(),
                'date_range_end': export.date_range_end.isoformat(),
                'created_at': export.created_at.isoformat(),
                'file_path': export.file_path.name if export.file_path else None,
                'is_active': export.is_active
            }
            data['analytics_exports'].append(export_data)

        # Salvar o backup
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        file_path = os.path.join(backup_dir, file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f'Backup realizado com sucesso em {file_path}'))

    def restore_data(self, file_path):
        """Restaura os dados do backup"""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Arquivo {file_path} não encontrado!'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Restaurar Sessões
        self.stdout.write('Restaurando sessões...')
        for session_data in data['sessions']:
            session, created = Session.objects.get_or_create(
                session_key=session_data['session_key'],
                defaults={
                    'ip_address': session_data['ip_address'],
                    'user_agent': session_data['user_agent'],
                    'referrer': session_data['referrer'],
                    'created_at': timezone.parse_datetime(session_data['created_at']),
                    'last_activity': timezone.parse_datetime(session_data['last_activity']),
                    'is_active': session_data['is_active']
                }
            )

        # Restaurar Cookies
        self.stdout.write('Restaurando cookies...')
        for cookie_data in data['cookies']:
            session = Session.objects.get(session_key=cookie_data['session_key'])
            cookie, created = Cookie.objects.get_or_create(
                name=cookie_data['name'],
                session=session,
                defaults={
                    'value': cookie_data['value'],
                    'domain': cookie_data['domain'],
                    'path': cookie_data['path'],
                    'expires': timezone.parse_datetime(cookie_data['expires']) if cookie_data['expires'] else None,
                    'secure': cookie_data['secure'],
                    'httponly': cookie_data['httponly'],
                    'samesite': cookie_data['samesite'],
                    'created_at': timezone.parse_datetime(cookie_data['created_at']),
                    'updated_at': timezone.parse_datetime(cookie_data['updated_at']),
                    'is_active': cookie_data['is_active']
                }
            )

        # Restaurar PageViews
        self.stdout.write('Restaurando visualizações de página...')
        for pageview_data in data['pageviews']:
            session = Session.objects.get(session_key=pageview_data['session_key'])
            pageview, created = PageView.objects.get_or_create(
                url=pageview_data['url'],
                session=session,
                created_at=timezone.parse_datetime(pageview_data['created_at']),
                defaults={
                    'title': pageview_data['title'],
                    'time_spent': pageview_data['time_spent'],
                    'is_active': pageview_data['is_active']
                }
            )

        # Restaurar SEO Metrics
        self.stdout.write('Restaurando métricas SEO...')
        for metric_data in data['seo_metrics']:
            metric, created = SEOMetrics.objects.get_or_create(
                url=metric_data['url'],
                defaults={
                    'title': metric_data['title'],
                    'meta_description': metric_data['meta_description'],
                    'h1_count': metric_data['h1_count'],
                    'h2_count': metric_data['h2_count'],
                    'h3_count': metric_data['h3_count'],
                    'image_count': metric_data['image_count'],
                    'word_count': metric_data['word_count'],
                    'internal_links': metric_data['internal_links'],
                    'external_links': metric_data['external_links'],
                    'last_checked': timezone.parse_datetime(metric_data['last_checked']),
                    'page_speed_score': metric_data['page_speed_score'],
                    'mobile_friendly_score': metric_data['mobile_friendly_score'],
                    'is_active': metric_data['is_active']
                }
            )

        # Restaurar Analytics Exports
        self.stdout.write('Restaurando exports de analytics...')
        for export_data in data['analytics_exports']:
            export, created = AnalyticsExport.objects.get_or_create(
                name=export_data['name'],
                created_at=timezone.parse_datetime(export_data['created_at']),
                defaults={
                    'format': export_data['format'],
                    'date_range_start': timezone.parse_datetime(export_data['date_range_start']).date(),
                    'date_range_end': timezone.parse_datetime(export_data['date_range_end']).date(),
                    'file_path': export_data['file_path'],
                    'is_active': export_data['is_active']
                }
            )

        self.stdout.write(self.style.SUCCESS('Restauração concluída com sucesso!')) 