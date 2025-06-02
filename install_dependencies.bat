@echo off
echo Installing dependencies...

:: Atualiza pip
python -m pip install --upgrade pip

:: Instala wheel primeiro
pip install wheel

:: Instala as dependências uma por uma para melhor controle de erros
pip install Django>=5.0.1
pip install django-browser-reload>=1.12.1
pip install django-compressor>=4.4
pip install rcssmin>=1.1.1
pip install rjsmin>=1.2.1
pip install django-bootstrap5==25.1
pip install django-environ==0.11.2
pip install gunicorn>=21.2.0
pip install whitenoise[brotli]>=6.6.0
pip install --only-binary :all: Pillow>=10.1.0
pip install psycopg2-binary>=2.9.9
pip install dj-database-url>=2.1.0
pip install python-dotenv>=1.0.0
pip install django-crispy-forms==2.1
pip install crispy-bootstrap5==2023.10
pip install django-cleanup==9.0.0
pip install django-redis==5.0.0
pip install redis==6.1.0
pip install djangorestframework==3.16.0
pip install django-filter==25.1
pip install django-user-agents==0.4.0
pip install python-dateutil==2.9.0.post0
pip install PyYAML==6.0.2
pip install requests==2.31.0
pip install urllib3==2.4.0
pip install django-cors-headers==4.3.1
pip install python-decouple==3.8
pip install XlsxWriter==3.1.9

echo Dependencies installed successfully!
pause 