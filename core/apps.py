from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'HOZ TECH Analytics'

    def ready(self):
        """
        Método chamado quando o aplicativo está pronto.
        Use para registrar sinais ou realizar outras inicializações.
        """
        try:
            import core.signals  # noqa
        except ImportError:
            pass 