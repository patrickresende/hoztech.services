from django.urls import path
from . import views

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
    # Landing Pages
    path('landingpages/', views.landing_pages, name='landing_pages'),
    path('landing/musico/', views.landing_musico, name='landing_musico'),
    path('landing/roupas/', views.landing_roupas, name='landing_roupas'),
    path('landing/salao/', views.landing_salao, name='landing_salao'),
    path('landing/limpeza/', views.landing_limpeza, name='landing_limpeza'),
]