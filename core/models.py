from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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