from django import forms
from django.core.validators import RegexValidator, validate_email
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
import re
from typing import Dict, Any


class ContactForm(forms.Form):
    NAME_MIN_LENGTH = 3
    NAME_MAX_LENGTH = 50
    EMAIL_MAX_LENGTH = 60
    PHONE_MAX_LENGTH = 15
    SUBJECT_MAX_LENGTH = 50
    MESSAGE_MIN_LENGTH = 50
    MESSAGE_MAX_LENGTH = 5000

    # Padrões de validação atualizados
    NAME_PATTERN = r'^[A-Za-zÀ-ÿ\s]+$'
    PHONE_PATTERN = r'^\d{8,15}$'  # Apenas números
    DANGEROUS_CONTENT_PATTERN = r'<script|javascript:|on\w+\s*=|data:|http[s]?://|www\.|\.com|\.br|\.org|\.net|\.io|\.co|\.me|\.tv|\.info|\.biz|\.cc|\.tk|\.ml|\.ga|\.cf|\.gq|\.xyz|\.top|\.club|\.online|\.site|\.web|\.app|\.dev|\.tech|\.digital|\.cloud|\.ai|\.io|\.ly|\.bit|\.ly|\.goo|\.gl|\.tiny|\.url|\.short|\.link|\.click|\.to|\.at|\.by|\.is|\.it|\.in|\.on|\.up|\.down|\.out|\.off|\.over|\.under|\.back|\.forward|\.next|\.prev|\.first|\.last|\.new|\.old|\.good|\.bad|\.best|\.worst|\.big|\.small|\.high|\.low|\.fast|\.slow|\.hot|\.cold|\.warm|\.cool|\.soft|\.hard|\.easy|\.hard|\.simple|\.complex|\.basic|\.advanced|\.pro|\.premium|\.vip|\.exclusive|\.limited|\.special|\.unique|\.rare|\.common|\.popular|\.trending|\.viral|\.famous|\.known|\.unknown|\.hidden|\.visible|\.public|\.private|\.secret|\.open|\.closed|\.locked|\.unlocked|\.secure|\.safe|\.dangerous|\.risky|\.careful|\.careless|\.smart|\.stupid|\.clever|\.dumb|\.wise|\.foolish|\.genius|\.idiot|\.expert|\.amateur|\.professional|\.beginner|\.master|\.student|\.teacher|\.leader|\.follower|\.boss|\.employee|\.manager|\.worker|\.director|\.assistant|\.helper|\.supporter|\.partner|\.friend|\.enemy|\.ally|\.rival|\.competitor|\.opponent|\.challenger|\.defender|\.attacker|\.winner|\.loser|\.champion|\.hero|\.villain|\.savior|\.destroyer|\.creator|\.builder|\.breaker|\.fixer|\.damager|\.healer|\.killer|\.protector|\.guardian|\.warrior|\.fighter|\.soldier|\.commander|\.general|\.captain|\.lieutenant|\.sergeant|\.private|\.officer|\.agent|\.spy|\.detective|\.investigator|\.researcher|\.scientist|\.engineer|\.developer|\.programmer|\.coder|\.hacker|\.cracker|\.phisher|\.spammer|\.scammer|\.fraudster|\.thief|\.robber|\.burglar|\.kidnapper|\.murderer|\.assassin|\.hitman|\.terrorist|\.extremist|\.radical|\.fanatic|\.zealot|\.cultist|\.worshipper|\.believer|\.skeptic|\.cynic|\.optimist|\.pessimist|\.realist|\.idealist|\.pragmatist|\.theorist|\.practitioner|\.academic|\.scholar|\.intellectual|\.philosopher|\.thinker|\.dreamer|\.visionary|\.prophet|\.oracle|\.seer|\.psychic|\.medium|\.shaman|\.witch|\.wizard|\.magician|\.sorcerer|\.warlock|\.necromancer|\.summoner|\.conjurer|\.enchanter|\.illusionist|\.transmuter|\.evoker|\.abjurer|\.diviner'

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
            'required': True,
            'style': 'text-transform: uppercase;'
        })
    )

    email = forms.EmailField(
        label=_("Email"),
        max_length=EMAIL_MAX_LENGTH,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('seu@email.com'),
            'autocomplete': 'email',
            'required': True,
            'maxlength': EMAIL_MAX_LENGTH
        })
    )

    phone = forms.CharField(
        label=_("Telefone"),
        max_length=PHONE_MAX_LENGTH,
        validators=[
            RegexValidator(
                regex=PHONE_PATTERN,
                message=_('O telefone deve conter apenas números (8-15 dígitos).'),
                code='invalid_phone'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Apenas números'),
            'autocomplete': 'tel',
            'required': True,
            'inputmode': 'numeric',
            'pattern': '[0-9]*'
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
        min_length=MESSAGE_MIN_LENGTH,
        max_length=MESSAGE_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Digite sua mensagem (mínimo 50 caracteres)'),
            'rows': 5,
            'required': True,
            'minlength': MESSAGE_MIN_LENGTH,
            'maxlength': MESSAGE_MAX_LENGTH
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
        
        # Converter para maiúsculas
        name = name.upper()
        
        # Verificar se contém apenas letras e espaços
        if not re.match(self.NAME_PATTERN, name):
            raise forms.ValidationError(_('O nome deve conter apenas letras e espaços.'))
        
        return name

    def clean_email(self) -> str:
        email = self.cleaned_data.get('email', '').strip().lower()
        
        # Verificar limite de caracteres
        if len(email) > self.EMAIL_MAX_LENGTH:
            raise forms.ValidationError(_(f'O email deve ter no máximo {self.EMAIL_MAX_LENGTH} caracteres.'))
        
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError(_('Por favor, insira um e-mail válido.'))
        
        return email

    def clean_phone(self) -> str:
        phone = self.cleaned_data.get('phone', '').strip()
        
        # Remover todos os caracteres não numéricos
        phone_digits = re.sub(r'\D', '', phone)
        
        if len(phone_digits) < 8 or len(phone_digits) > 15:
            raise forms.ValidationError(_('O telefone deve ter entre 8 e 15 dígitos.'))
        
        return phone_digits

    def clean_subject(self) -> str:
        subject = strip_tags(self.cleaned_data.get('subject', '')).strip()
        if not subject:
            raise forms.ValidationError(_('O campo assunto é obrigatório.'))
        if len(subject) > self.SUBJECT_MAX_LENGTH:
            raise forms.ValidationError(_(f'O assunto deve ter no máximo {self.SUBJECT_MAX_LENGTH} caracteres.'))
        
        # Verificar conteúdo malicioso
        if re.search(self.DANGEROUS_CONTENT_PATTERN, subject, flags=re.I):
            raise forms.ValidationError(_('O assunto contém conteúdo potencialmente perigoso.'))
        
        return subject

    def clean_message(self) -> str:
        message = strip_tags(self.cleaned_data.get('message', '')).strip()
        
        # Verificar tamanho mínimo e máximo
        if len(message) < self.MESSAGE_MIN_LENGTH:
            raise forms.ValidationError(_(f'A mensagem deve ter pelo menos {self.MESSAGE_MIN_LENGTH} caracteres.'))
        
        if len(message) > self.MESSAGE_MAX_LENGTH:
            raise forms.ValidationError(_(f'A mensagem deve ter no máximo {self.MESSAGE_MAX_LENGTH} caracteres.'))
        
        # Verificar conteúdo malicioso
        if re.search(self.DANGEROUS_CONTENT_PATTERN, message, flags=re.I):
            raise forms.ValidationError(_('A mensagem contém conteúdo potencialmente perigoso.'))
        
        # Verificar links suspeitos
        suspicious_patterns = [
            r'http[s]?://',
            r'www\.',
            r'\.com',
            r'\.br',
            r'\.org',
            r'\.net',
            r'\.io',
            r'\.co',
            r'\.me',
            r'\.tv',
            r'\.info',
            r'\.biz',
            r'\.cc',
            r'\.tk',
            r'\.ml',
            r'\.ga',
            r'\.cf',
            r'\.gq',
            r'\.xyz',
            r'\.top',
            r'\.club',
            r'\.online',
            r'\.site',
            r'\.web',
            r'\.app',
            r'\.dev',
            r'\.tech',
            r'\.digital',
            r'\.cloud',
            r'\.ai',
            r'\.ly',
            r'\.bit',
            r'\.goo',
            r'\.gl',
            r'\.tiny',
            r'\.url',
            r'\.short',
            r'\.link',
            r'\.click',
            r'\.to',
            r'\.at',
            r'\.by',
            r'\.is',
            r'\.it',
            r'\.in',
            r'\.on',
            r'\.up',
            r'\.down',
            r'\.out',
            r'\.off',
            r'\.over',
            r'\.under',
            r'\.back',
            r'\.forward',
            r'\.next',
            r'\.prev',
            r'\.first',
            r'\.last',
            r'\.new',
            r'\.old',
            r'\.good',
            r'\.bad',
            r'\.best',
            r'\.worst',
            r'\.big',
            r'\.small',
            r'\.high',
            r'\.low',
            r'\.fast',
            r'\.slow',
            r'\.hot',
            r'\.cold',
            r'\.warm',
            r'\.cool',
            r'\.soft',
            r'\.hard',
            r'\.easy',
            r'\.simple',
            r'\.complex',
            r'\.basic',
            r'\.advanced',
            r'\.pro',
            r'\.premium',
            r'\.vip',
            r'\.exclusive',
            r'\.limited',
            r'\.special',
            r'\.unique',
            r'\.rare',
            r'\.common',
            r'\.popular',
            r'\.trending',
            r'\.viral',
            r'\.famous',
            r'\.known',
            r'\.unknown',
            r'\.hidden',
            r'\.visible',
            r'\.public',
            r'\.private',
            r'\.secret',
            r'\.open',
            r'\.closed',
            r'\.locked',
            r'\.unlocked',
            r'\.secure',
            r'\.safe',
            r'\.dangerous',
            r'\.risky',
            r'\.careful',
            r'\.careless',
            r'\.smart',
            r'\.stupid',
            r'\.clever',
            r'\.dumb',
            r'\.wise',
            r'\.foolish',
            r'\.genius',
            r'\.idiot',
            r'\.expert',
            r'\.amateur',
            r'\.professional',
            r'\.beginner',
            r'\.master',
            r'\.student',
            r'\.teacher',
            r'\.leader',
            r'\.follower',
            r'\.boss',
            r'\.employee',
            r'\.manager',
            r'\.worker',
            r'\.director',
            r'\.assistant',
            r'\.helper',
            r'\.supporter',
            r'\.partner',
            r'\.friend',
            r'\.enemy',
            r'\.ally',
            r'\.rival',
            r'\.competitor',
            r'\.opponent',
            r'\.challenger',
            r'\.defender',
            r'\.attacker',
            r'\.winner',
            r'\.loser',
            r'\.champion',
            r'\.hero',
            r'\.villain',
            r'\.savior',
            r'\.destroyer',
            r'\.creator',
            r'\.builder',
            r'\.breaker',
            r'\.fixer',
            r'\.damager',
            r'\.healer',
            r'\.killer',
            r'\.protector',
            r'\.guardian',
            r'\.warrior',
            r'\.fighter',
            r'\.soldier',
            r'\.commander',
            r'\.general',
            r'\.captain',
            r'\.lieutenant',
            r'\.sergeant',
            r'\.private',
            r'\.officer',
            r'\.agent',
            r'\.spy',
            r'\.detective',
            r'\.investigator',
            r'\.researcher',
            r'\.scientist',
            r'\.engineer',
            r'\.developer',
            r'\.programmer',
            r'\.coder',
            r'\.hacker',
            r'\.cracker',
            r'\.phisher',
            r'\.spammer',
            r'\.scammer',
            r'\.fraudster',
            r'\.thief',
            r'\.robber',
            r'\.burglar',
            r'\.kidnapper',
            r'\.murderer',
            r'\.assassin',
            r'\.hitman',
            r'\.terrorist',
            r'\.extremist',
            r'\.radical',
            r'\.fanatic',
            r'\.zealot',
            r'\.cultist',
            r'\.worshipper',
            r'\.believer',
            r'\.skeptic',
            r'\.cynic',
            r'\.optimist',
            r'\.pessimist',
            r'\.realist',
            r'\.idealist',
            r'\.pragmatist',
            r'\.theorist',
            r'\.practitioner',
            r'\.academic',
            r'\.scholar',
            r'\.intellectual',
            r'\.philosopher',
            r'\.thinker',
            r'\.dreamer',
            r'\.visionary',
            r'\.prophet',
            r'\.oracle',
            r'\.seer',
            r'\.psychic',
            r'\.medium',
            r'\.shaman',
            r'\.witch',
            r'\.wizard',
            r'\.magician',
            r'\.sorcerer',
            r'\.warlock',
            r'\.necromancer',
            r'\.summoner',
            r'\.conjurer',
            r'\.enchanter',
            r'\.illusionist',
            r'\.transmuter',
            r'\.evoker',
            r'\.abjurer',
            r'\.diviner'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, message, flags=re.I):
                raise forms.ValidationError(_('A mensagem contém links ou conteúdo suspeito.'))
        
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
