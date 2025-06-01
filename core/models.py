from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Cookie(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    domain = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    expires = models.DateTimeField(null=True, blank=True)
    secure = models.BooleanField(default=False)
    httponly = models.BooleanField(default=False)
    samesite = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='cookies')

    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookies'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.domain}"

class Session(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['-last_activity']

    def __str__(self):
        return f"Session {self.session_key} - {self.ip_address}"

class PageView(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='page_views')
    url = models.URLField()
    title = models.CharField(max_length=255)
    time_spent = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.url} - {self.created_at}"

class SEOMetrics(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    meta_description = models.TextField()
    h1_count = models.IntegerField(default=0)
    h2_count = models.IntegerField(default=0)
    h3_count = models.IntegerField(default=0)
    image_count = models.IntegerField(default=0)
    word_count = models.IntegerField(default=0)
    internal_links = models.IntegerField(default=0)
    external_links = models.IntegerField(default=0)
    last_checked = models.DateTimeField(auto_now=True)
    page_speed_score = models.FloatField(null=True, blank=True)
    mobile_friendly_score = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = 'SEO Metrics'
        verbose_name_plural = 'SEO Metrics'
        ordering = ['-last_checked']

    def __str__(self):
        return f"{self.url} - {self.title}"

class AnalyticsExport(models.Model):
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
        ('pdf', 'PDF'),
    ]

    name = models.CharField(max_length=255)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='analytics_exports/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Analytics Export'
        verbose_name_plural = 'Analytics Exports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.format}" 