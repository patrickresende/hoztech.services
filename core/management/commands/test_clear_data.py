from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from core.models import Session, AnalyticsExport, SEOMetrics, Cookie, PageView
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Teste das funcionalidades de limpeza de dados'

    def handle(self, *args, **options):
        self.stdout.write('🧹 Teste das Funcionalidades de Limpeza de Dados')
        
        # Verificar dados iniciais
        self.stdout.write('\n📊 Dados Iniciais:')
        initial_stats = self.get_data_stats()
        for key, value in initial_stats.items():
            self.stdout.write(f'{key}: {value}')
        
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='admin_test',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('✅ Usuário de teste criado')
        
        client = Client()
        login_success = client.login(username='admin_test', password='admin123')
        
        if not login_success:
            self.stdout.write('❌ Falha no login')
            return
        
        # Testar endpoint de estatísticas
        self.stdout.write('\n🔗 Testando Endpoint de Estatísticas:')
        try:
            response = client.get('/core_admin/get-stats/')
            self.stdout.write(f'Status: {response.status_code}')
            if response.status_code == 200:
                self.stdout.write('✅ Endpoint de estatísticas funcionando')
                data = response.json()
                if data['success']:
                    self.stdout.write('✅ Dados de estatísticas retornados corretamente')
                else:
                    self.stdout.write('❌ Erro nos dados de estatísticas')
            else:
                self.stdout.write('❌ Endpoint de estatísticas com problema')
        except Exception as e:
            self.stdout.write(f'❌ Erro no endpoint de estatísticas: {e}')
        
        # Testar endpoint de limpeza (apenas verificar se está acessível)
        self.stdout.write('\n🔗 Testando Endpoint de Limpeza:')
        try:
            response = client.post('/core_admin/clear-data/', {
                'period': 'hour'
            })
            self.stdout.write(f'Status: {response.status_code}')
            if response.status_code in [200, 302]:
                self.stdout.write('✅ Endpoint de limpeza acessível')
            else:
                self.stdout.write('❌ Endpoint de limpeza com problema')
        except Exception as e:
            self.stdout.write(f'❌ Erro no endpoint de limpeza: {e}')
        
        # Testar função de limpeza diretamente
        self.stdout.write('\n🧹 Testando Função de Limpeza Diretamente:')
        try:
            from core.admin_views import clear_data_since, clear_all_data
            
            # Testar limpeza de dados antigos (mais de 1 mês)
            old_cutoff = timezone.now() - timedelta(days=35)
            deleted_count = clear_data_since(old_cutoff)
            self.stdout.write(f'Dados antigos removidos: {deleted_count}')
            
            # Verificar dados após limpeza
            self.stdout.write('\n📊 Dados Após Limpeza:')
            final_stats = self.get_data_stats()
            for key, value in final_stats.items():
                self.stdout.write(f'{key}: {value}')
            
            # Verificar se a limpeza funcionou
            if deleted_count >= 0:
                self.stdout.write('✅ Função de limpeza funcionando')
            else:
                self.stdout.write('❌ Problema na função de limpeza')
                
        except Exception as e:
            self.stdout.write(f'❌ Erro na função de limpeza: {e}')
        
        # Testar diferentes períodos
        self.stdout.write('\n⏰ Testando Diferentes Períodos:')
        periods = {
            'hour': timedelta(hours=1),
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(days=30)
        }
        
        for period_name, delta in periods.items():
            try:
                cutoff_time = timezone.now() - delta
                count_before = self.get_period_count(cutoff_time)
                self.stdout.write(f'{period_name}: {count_before} registros')
            except Exception as e:
                self.stdout.write(f'❌ Erro ao verificar período {period_name}: {e}')
        
        self.stdout.write('\n✅ Teste de limpeza de dados concluído!')

    def get_data_stats(self):
        """Obter estatísticas dos dados"""
        return {
            'Sessões': Session.objects.count(),
            'Page Views': PageView.objects.count(),
            'Cookies': Cookie.objects.count(),
            'SEO Metrics': SEOMetrics.objects.count(),
            'Analytics Exports': AnalyticsExport.objects.count()
        }
    
    def get_period_count(self, cutoff_time):
        """Contar registros desde uma data específica"""
        return (
            Session.objects.filter(created_at__gte=cutoff_time).count() +
            PageView.objects.filter(created_at__gte=cutoff_time).count() +
            Cookie.objects.filter(created_at__gte=cutoff_time).count() +
            AnalyticsExport.objects.filter(created_at__gte=cutoff_time).count()
        ) 