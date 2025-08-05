from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
from django.core.exceptions import ValidationError

class Cookie(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    value = models.TextField()
    domain = models.CharField(max_length=255, db_index=True)
    path = models.CharField(max_length=255)
    expires = models.DateTimeField(null=True, blank=True, db_index=True)
    secure = models.BooleanField(default=False)
    httponly = models.BooleanField(default=False)
    samesite = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='cookies')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'domain']),
            models.Index(fields=['created_at', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.name} - {self.domain}"

class Session(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField()
    referrer = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_activity = models.DateTimeField(auto_now=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['created_at', 'is_active']),
            models.Index(fields=['last_activity', 'is_active']),
            models.Index(fields=['ip_address', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Session {self.session_key} - {self.ip_address}"

class PageView(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='page_views')
    url = models.URLField(db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    time_spent = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['url', 'created_at']),
            models.Index(fields=['created_at', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.url} - {self.created_at}"

class SEOMetrics(models.Model):
    url = models.URLField(unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    meta_description = models.TextField()
    h1_count = models.IntegerField(default=0)
    h2_count = models.IntegerField(default=0)
    h3_count = models.IntegerField(default=0)
    image_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    internal_links = models.IntegerField(default=0)
    external_links = models.IntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True, db_index=True)
    page_speed_score = models.FloatField(null=True, blank=True, db_index=True)
    mobile_friendly_score = models.FloatField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seo_metrics_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='seo_metrics_updated')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'SEO Metrics'
        verbose_name_plural = 'SEO Metrics'
        ordering = ['-last_checked']
        indexes = [
            models.Index(fields=['url', 'is_active']),
            models.Index(fields=['last_checked', 'is_active']),
            models.Index(fields=['page_speed_score', 'mobile_friendly_score']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.url} - {self.title}"

class AnalyticsExport(models.Model):
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
        ('pdf', 'PDF'),
    ]

    name = models.CharField(max_length=255, db_index=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    date_range_start = models.DateField(db_index=True)
    date_range_end = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    file_path = models.FileField(upload_to='analytics_exports/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'Analytics Export'
        verbose_name_plural = 'Analytics Exports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['date_range_start', 'date_range_end']),
            models.Index(fields=['created_at', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.name} - {self.format}"


# ===== MODELOS DO CHATBOT WHATSAPP =====

class WhatsAppContact(models.Model):
    """Modelo para gerenciar contatos do WhatsApp"""
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    is_blocked = models.BooleanField(default=False, db_index=True)
    is_my_contact = models.BooleanField(default=False, db_index=True)  # Para filtrar sua lista de contatos
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'WhatsApp Contact'
        verbose_name_plural = 'WhatsApp Contacts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number', 'is_active']),
            models.Index(fields=['is_my_contact', 'is_blocked']),
            models.Index(fields=['created_at', 'is_active']),
        ]

    def clean(self):
        # Validar formato do número de telefone
        if not self.phone_number.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValidationError('Número de telefone deve conter apenas dígitos, +, - e espaços')

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.name or 'Sem nome'} - {self.phone_number}"


class WhatsAppSession(models.Model):
    """Modelo para gerenciar sessões de conversas automatizadas"""
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('paused', 'Pausada'),
        ('completed', 'Concluída'),
        ('error', 'Erro'),
    ]

    contact = models.ForeignKey(WhatsAppContact, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    current_step = models.IntegerField(default=0)
    context_data = models.JSONField(default=dict, blank=True)  # Para armazenar dados da conversa
    started_at = models.DateTimeField(auto_now_add=True, db_index=True)
    last_activity = models.DateTimeField(auto_now=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'WhatsApp Session'
        verbose_name_plural = 'WhatsApp Sessions'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['session_id', 'is_active']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['started_at', 'status']),
            models.Index(fields=['last_activity', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"Sessão {self.session_id} - {self.contact.phone_number}"


class WhatsAppMessage(models.Model):
    """Modelo para armazenar mensagens do WhatsApp"""
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('document', 'Documento'),
        ('audio', 'Áudio'),
        ('video', 'Vídeo'),
        ('location', 'Localização'),
        ('contact', 'Contato'),
    ]

    DIRECTION_CHOICES = [
        ('incoming', 'Recebida'),
        ('outgoing', 'Enviada'),
    ]

    session = models.ForeignKey(WhatsAppSession, on_delete=models.CASCADE, related_name='messages')
    message_id = models.CharField(max_length=100, unique=True, db_index=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, db_index=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    media_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(db_index=True)
    is_automated = models.BooleanField(default=False, db_index=True)  # Se foi enviada pelo bot
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'WhatsApp Message'
        verbose_name_plural = 'WhatsApp Messages'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['message_id', 'is_active']),
            models.Index(fields=['direction', 'is_automated']),
            models.Index(fields=['timestamp', 'is_active']),
            models.Index(fields=['session', 'timestamp']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.direction} - {self.session.contact.phone_number} - {self.timestamp}"


class WhatsAppTemplate(models.Model):
    """Modelo para templates de mensagens automatizadas"""
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    content = models.TextField()
    variables = models.JSONField(default=list, blank=True)  # Lista de variáveis no template
    step_number = models.IntegerField(default=0, db_index=True)  # Para sequência de mensagens
    delay_seconds = models.IntegerField(default=0)  # Delay antes de enviar
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'WhatsApp Template'
        verbose_name_plural = 'WhatsApp Templates'
        ordering = ['step_number', 'name']
        indexes = [
            models.Index(fields=['name', 'is_active']),
            models.Index(fields=['step_number', 'is_active']),
            models.Index(fields=['created_at', 'is_active']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def render_content(self, context_data=None):
        """Renderiza o template com os dados do contexto"""
        if not context_data:
            return self.content
        
        content = self.content
        for key, value in context_data.items():
            content = content.replace(f"{{{key}}}", str(value))
        return content

    def __str__(self):
        return f"{self.name} - Passo {self.step_number}"


class WhatsAppConfig(models.Model):
    """Configurações do sistema de chatbot"""
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'WhatsApp Config'
        verbose_name_plural = 'WhatsApp Configs'
        ordering = ['key']

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    @classmethod
    def get_value(cls, key, default=None):
        """Método helper para obter valores de configuração"""
        try:
            config = cls.objects.get(key=key, is_active=True)
            return config.value
        except cls.DoesNotExist:
            return default

    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."


class WhatsAppLog(models.Model):
    """Log de atividades do chatbot"""
    LOG_LEVEL_CHOICES = [
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]

    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, db_index=True)
    message = models.TextField()
    session = models.ForeignKey(WhatsAppSession, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.ForeignKey(WhatsAppContact, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'WhatsApp Log'
        verbose_name_plural = 'WhatsApp Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['level', 'timestamp']),
            models.Index(fields=['timestamp', 'is_active']),
            models.Index(fields=['session', 'timestamp']),
        ]

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"[{self.level.upper()}] {self.message[:100]}..."