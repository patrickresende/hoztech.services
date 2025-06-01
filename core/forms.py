from django import forms
from django.core.validators import RegexValidator
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
import re
from typing import Dict, Any

class ContactForm(forms.Form):
    """Formulário de contato com validação robusta"""
    
    # Constantes
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 50
    PHONE_MIN_LENGTH = 8
    PHONE_MAX_LENGTH = 15
    SUBJECT_MAX_LENGTH = 20
    MESSAGE_MAX_LENGTH = 5000
    
    # Regex patterns
    NAME_PATTERN = r'^[A-Za-zÀ-ÿ\s]{3,50}$'
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE_PATTERN = r'^\(\d{2}\) \d{5}-\d{4}$'
    DANGEROUS_CONTENT_PATTERN = r'<script|javascript:|on\w+\s*=|data:'
    
    # Campos do formulário
    name = forms.CharField(
        max_length=NAME_MAX_LENGTH,
        min_length=NAME_MIN_LENGTH,
        validators=[
            RegexValidator(
                regex=NAME_PATTERN,
                message=_('O nome deve conter apenas letras e espaços (3-50 caracteres)')
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Seu nome completo'),
            'required': True,
            'autocomplete': 'name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('seu@email.com'),
            'required': True,
            'autocomplete': 'email'
        })
    )
    
    phone = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=PHONE_PATTERN,
                message=_('O telefone deve estar no formato (99) 99999-9999')
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('(99) 99999-9999'),
            'required': True,
            'autocomplete': 'tel'
        })
    )
    
    subject = forms.CharField(
        max_length=SUBJECT_MAX_LENGTH,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Assunto da mensagem'),
            'required': True
        })
    )
    
    message = forms.CharField(
        max_length=MESSAGE_MAX_LENGTH,
        min_length=1,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Digite sua mensagem'),
            'rows': 5,
            'required': True
        })
    )
    
    # Campo honeypot para prevenir spam
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'style': 'display: none;',
            'autocomplete': 'off'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove website from required fields
        if 'website' in self.fields:
            self.fields['website'].required = False
    
    def clean_name(self) -> str:
        """Sanitiza e valida o nome"""
        name = self.cleaned_data['name']
        name = strip_tags(name).strip()
        
        if not re.match(self.NAME_PATTERN, name):
            raise forms.ValidationError(_('O nome deve conter apenas letras e espaços (3-50 caracteres)'))
        
        return name
    
    def clean_email(self) -> str:
        """Valida o email"""
        email = self.cleaned_data['email'].lower()
        
        if not re.match(self.EMAIL_PATTERN, email):
            raise forms.ValidationError(_('Formato de email inválido'))
        
        return email
    
    def clean_phone(self) -> str:
        """Sanitiza e valida o telefone"""
        phone = self.cleaned_data['phone']
        # Remove caracteres não numéricos para validação
        phone_numbers = re.sub(r'\D', '', phone)
        
        if len(phone_numbers) < 10 or len(phone_numbers) > 11:
            raise forms.ValidationError(_('O telefone deve ter 10 ou 11 dígitos'))
        
        # Mantém o formato original para exibição
        return phone
    
    def clean_subject(self) -> str:
        """Sanitiza e valida o assunto"""
        subject = self.cleaned_data['subject']
        subject = strip_tags(subject).strip()
        
        if len(subject) > self.SUBJECT_MAX_LENGTH:
            raise forms.ValidationError(_('O assunto deve ter no máximo 20 caracteres'))
        
        return subject
    
    def clean_message(self) -> str:
        """Sanitiza e valida a mensagem"""
        message = self.cleaned_data['message']
        # Remove HTML e conteúdo potencialmente perigoso
        message = strip_tags(message)
        message = re.sub(self.DANGEROUS_CONTENT_PATTERN, '', message, flags=re.I)
        
        if len(message) > self.MESSAGE_MAX_LENGTH:
            raise forms.ValidationError(_('A mensagem deve ter no máximo 5000 caracteres'))
        
        return message.strip()
    
    def clean_website(self) -> str:
        """Valida o campo honeypot"""
        website = self.cleaned_data.get('website', '')
        if website:  # Se o campo foi preenchido, é provavelmente um bot
            raise forms.ValidationError(_('Form submission failed'))
        return website
    
    def get_cleaned_data(self) -> Dict[str, Any]:
        """Retorna os dados sanitizados do formulário"""
        data = self.cleaned_data.copy()
        # Remove website from cleaned data
        data.pop('website', None)
        return data 