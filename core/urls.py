from django.urls import path
from . import views
from .whatsapp_views import (
    WhatsAppWebhookView, WhatsAppDashboardView, WhatsAppContactsView,
    WhatsAppTemplatesView, WhatsAppConfigView, WhatsAppSendMessageView,
    WhatsAppSendMessagePageView, whatsapp_cleanup, whatsapp_health
)

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre_nos, name='sobre_nos'),
    path('servicos/', views.services, name='services'),
    path('minha-seguranca/', views.minha_seguranca, name='minha_seguranca'),
    path('contato/', views.contact, name='contact'),
    path('privacidade/', views.privacy, name='privacy'),
    path('termos/', views.terms, name='terms'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('faq/', views.faq, name='faq'),
    path('security-policy/', views.security_policy, name='security_policy'),
    path('exclusao-de-dados/', views.exclusao_dados, name='exclusao_dados'),
    # Landing Pages
    path('landingpages/', views.landing_pages, name='landing_pages'),
    path('landing/musico/', views.landing_musico, name='landing_musico'),
    path('landing/roupas/', views.landing_roupas, name='landing_roupas'),
    path('landing/salao/', views.landing_salao, name='landing_salao'),
    path('landing/limpeza/', views.landing_limpeza, name='landing_limpeza'),
    
    # WhatsApp Chatbot URLs (Backend apenas - sem renderização pública)
    path('chatbot/webhook/', WhatsAppWebhookView.as_view(), name='whatsapp_webhook'),
    path('chatbot/dashboard/', WhatsAppDashboardView.as_view(), name='whatsapp_dashboard'),
    path('chatbot/contacts/', WhatsAppContactsView.as_view(), name='whatsapp_contacts'),
    path('chatbot/templates/', WhatsAppTemplatesView.as_view(), name='whatsapp_templates'),
    path('chatbot/config/', WhatsAppConfigView.as_view(), name='whatsapp_config'),
    path('chatbot/send-message/', WhatsAppSendMessageView.as_view(), name='whatsapp_send_message'),
    path('chatbot/send/', WhatsAppSendMessagePageView.as_view(), name='whatsapp_send_page'),
    path('chatbot/cleanup/', whatsapp_cleanup, name='whatsapp_cleanup'),
    path('chatbot/health/', whatsapp_health, name='whatsapp_health'),
]