from django.core.management.base import BaseCommand
from django.db import connection, DatabaseError
from django.conf import settings
import os
import time

class Command(BaseCommand):
    help = 'Verifica a conectividade e configuração do banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Mostra informações detalhadas',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(
            self.style.SUCCESS('=== Verificação de Banco de Dados ===')
        )
        
        # 1. Verificar variáveis de ambiente
        self.stdout.write('\n1. Verificando variáveis de ambiente...')
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            # Mascarar senha para segurança
            masked_url = self._mask_database_url(database_url)
            self.stdout.write(f'✓ DATABASE_URL: {masked_url}')
        else:
            self.stdout.write(self.style.WARNING('⚠ DATABASE_URL não encontrada'))
            
        # 2. Verificar configurações do Django
        self.stdout.write('\n2. Verificando configurações do Django...')
        db_config = settings.DATABASES['default']
        self.stdout.write(f'✓ Engine: {db_config.get("ENGINE", "N/A")}')
        self.stdout.write(f'✓ Name: {db_config.get("NAME", "N/A")}')
        self.stdout.write(f'✓ Host: {db_config.get("HOST", "N/A")}')
        self.stdout.write(f'✓ Port: {db_config.get("PORT", "N/A")}')
        self.stdout.write(f'✓ User: {db_config.get("USER", "N/A")}')
        
        if verbose:
            self.stdout.write(f'✓ CONN_MAX_AGE: {db_config.get("CONN_MAX_AGE", "N/A")}')
            self.stdout.write(f'✓ Options: {db_config.get("OPTIONS", {})}')
        
        # 3. Testar conexão
        self.stdout.write('\n3. Testando conexão...')
        try:
            start_time = time.time()
            connection.ensure_connection()
            connection_time = time.time() - start_time
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Conexão bem-sucedida em {connection_time:.3f}s')
            )
            
            # Verificar se a conexão está ativa
            if connection.connection:
                self.stdout.write('✓ Conexão ativa')
            else:
                self.stdout.write(self.style.WARNING('⚠ Conexão não está ativa'))
                
        except DatabaseError as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro de conexão: {e}')
            )
            return
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro inesperado: {e}')
            )
            return
        
        # 4. Testar query simples
        self.stdout.write('\n4. Testando query simples...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result and result[0] == 1:
                    self.stdout.write(self.style.SUCCESS('✓ Query de teste bem-sucedida'))
                else:
                    self.stdout.write(self.style.WARNING('⚠ Query retornou resultado inesperado'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro na query: {e}')
            )
        
        # 5. Verificar tabelas do sistema
        self.stdout.write('\n5. Verificando tabelas do sistema...')
        try:
            with connection.cursor() as cursor:
                if 'postgresql' in db_config.get('ENGINE', ''):
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name IN ('django_migrations', 'auth_user')
                        ORDER BY table_name
                    """)
                elif 'sqlite' in db_config.get('ENGINE', ''):
                    cursor.execute("""
                        SELECT name 
                        FROM sqlite_master 
                        WHERE type='table' 
                        AND name IN ('django_migrations', 'auth_user')
                        ORDER BY name
                    """)
                
                tables = cursor.fetchall()
                if tables:
                    for table in tables:
                        self.stdout.write(f'✓ Tabela encontrada: {table[0]}')
                else:
                    self.stdout.write(self.style.WARNING('⚠ Tabelas do sistema não encontradas'))
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Erro ao verificar tabelas: {e}')
            )
        
        # 6. Verificar configurações de SSL (PostgreSQL)
        if 'postgresql' in db_config.get('ENGINE', ''):
            self.stdout.write('\n6. Verificando configurações SSL...')
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SHOW ssl")
                    ssl_result = cursor.fetchone()
                    if ssl_result:
                        self.stdout.write(f'✓ SSL: {ssl_result[0]}')
                    else:
                        self.stdout.write('✓ SSL: Configuração padrão')
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Não foi possível verificar SSL: {e}')
                )
        
        # 7. Verificar configurações de timeout
        self.stdout.write('\n7. Verificando timeouts...')
        try:
            with connection.cursor() as cursor:
                if 'postgresql' in db_config.get('ENGINE', ''):
                    cursor.execute("SHOW statement_timeout")
                    timeout_result = cursor.fetchone()
                    if timeout_result:
                        self.stdout.write(f'✓ Statement timeout: {timeout_result[0]}')
                    
                    cursor.execute("SHOW idle_in_transaction_session_timeout")
                    idle_result = cursor.fetchone()
                    if idle_result:
                        self.stdout.write(f'✓ Idle timeout: {idle_result[0]}')
                else:
                    self.stdout.write('✓ Timeouts: Configuração padrão (SQLite)')
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠ Não foi possível verificar timeouts: {e}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n=== Verificação concluída ===')
        )
        
        if verbose:
            self.stdout.write(
                self.style.SUCCESS('\nPara mais informações, verifique os logs do sistema.')
            )

    def _mask_database_url(self, url):
        """Mascara a senha na URL do banco para segurança"""
        if '@' in url and ':' in url:
            parts = url.split('@')
            if len(parts) == 2:
                auth_part = parts[0]
                rest_part = parts[1]
                
                if '://' in auth_part:
                    protocol_part = auth_part.split('://')[0] + '://'
                    credentials_part = auth_part.split('://')[1]
                    
                    if ':' in credentials_part:
                        username = credentials_part.split(':')[0]
                        return f"{protocol_part}{username}:***@{rest_part}"
        
        return url 