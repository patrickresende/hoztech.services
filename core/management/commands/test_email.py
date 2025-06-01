from django.core.management.base import BaseCommand
from tests import run_all_tests

class Command(BaseCommand):
    help = 'Executa testes do sistema de email'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando testes do sistema de email...'))
        results = run_all_tests()
        
        # Exibe resultados formatados
        for test_name, (success, message) in results.items():
            if success:
                self.stdout.write(self.style.SUCCESS(f'✅ {test_name}: {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ {test_name}: {message}')) 