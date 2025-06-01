from django.conf import settings

def site_settings(request):
    """
    Add site settings to template context.
    """
    return {
        'SITE_NAME': settings.SITE_NAME,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
    } 