from django.urls import path, include
from . import views
from typing import List

app_name = 'core'

# URL patterns organized by feature
urlpatterns: List[path] = [
    # Main pages
    path('', views.home, name='home'),
    path('sobre/', views.sobre_nos, name='sobre'),
    path('servicos/', views.services, name='servicos'),
    path('minha-seguranca/', views.minha_seguranca, name='minha_seguranca'),
    
    # Contact related
    path('contato/', views.contact, name='contact'),
    
    # Legal pages
    path('privacidade/', views.privacy, name='privacy'),
    path('termos/', views.terms, name='terms'),
    
    # Resources
    path('download-pdf/', views.download_pdf, name='download_pdf'),
] 