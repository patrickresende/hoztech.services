from django import forms
from django.core.validators import RegexValidator, validate_email
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
import re
from typing import Dict, Any


class ContactForm(forms.Form):
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 50
    PHONE_MAX_LENGTH = 15
    SUBJECT_MAX_LENGTH = 50
    MESSAGE_MAX_LENGTH = 5000

    # Padrões de validação
    NAME_PATTERN = r'^[A-Za-zÀ-ÿ\s]+$'
    PHONE_PATTERN = r'^\(\d{2}\) \d{4,5}-\d{4}$'
    DANGEROUS_CONTENT_PATTERN = r'<script|javascript:|on\w+\s*=|data:'

    # Campos
    name = forms.CharField(
        label=_("Nome"),
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=NAME_PATTERN,
                message=_('O nome deve conter apenas letras e espaços.'),
                code='invalid_name'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Seu nome completo'),
            'autocomplete': 'name',
            'required': True
        })
    )

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('seu@email.com'),
            'autocomplete': 'email',
            'required': True
        })
    )

    phone = forms.CharField(
        label=_("Telefone"),
        max_length=PHONE_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=PHONE_PATTERN,
                message=_('Use o formato (99) 99999-9999 ou (99) 9999-9999'),
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('(99) 99999-9999'),
            'autocomplete': 'tel',
            'required': True
        })
    )

    subject = forms.CharField(
        label=_("Assunto"),
        max_length=SUBJECT_MAX_LENGTH,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Assunto da mensagem'),
            'required': True
        })
    )

    message = forms.CharField(
        label=_("Mensagem"),
        max_length=MESSAGE_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Digite sua mensagem'),
            'rows': 5,
            'required': True
        })
    )

    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'autocomplete': 'off',
            'aria-hidden': 'true'
        })
    )

    def clean_name(self) -> str:
        name = strip_tags(self.cleaned_data.get('name', '')).strip()
        if len(name) < self.NAME_MIN_LENGTH or len(name) > self.NAME_MAX_LENGTH:
            raise forms.ValidationError(_('O nome deve ter entre 3 e 50 caracteres.'))
        return name

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email', '').strip().lower()
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError(_('Por favor, insira um e-mail válido.'))
        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get('phone', '').strip()
        phone_digits = re.sub(r'\D', '', phone)
        if len(phone_digits) not in (10, 11):
            raise forms.ValidationError(_('O telefone deve ter 10 ou 11 dígitos.'))
        return phone

    def clean_subject(self) -> str:
        subject = strip_tags(self.cleaned_data.get('subject', '')).strip()
        if not subject:
            raise forms.ValidationError(_('O campo assunto é obrigatório.'))
        if len(subject) > self.SUBJECT_MAX_LENGTH:
            raise forms.ValidationError(_(f'O assunto deve ter no máximo {self.SUBJECT_MAX_LENGTH} caracteres.'))
        return subject

    def clean_message(self) -> str:
        message = strip_tags(self.cleaned_data.get('message', '')).strip()
        if re.search(self.DANGEROUS_CONTENT_PATTERN, message, flags=re.I):
            raise forms.ValidationError(_('A mensagem contém conteúdo potencialmente perigoso.'))
        return message

    def clean_website(self) -> str:
        website = self.cleaned_data.get('website', '').strip()
        if website:
            raise forms.ValidationError(_('Envio inválido detectado.'))
        return website

    def get_cleaned_data(self) -> Dict[str, Any]:
        data = self.cleaned_data.copy()
        data.pop('website', None)
        return data
