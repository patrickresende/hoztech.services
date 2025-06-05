#!/usr/bin/env bash
# Exit on error
set -o errexit

# Função para verificar arquivos
check_files() {
    local dir=$1
    local pattern=$2
    echo "Verificando arquivos em $dir com padrão $pattern"
    for file in $dir/$pattern; do
        if [ -f "$file" ]; then
            echo "✓ Arquivo existe: $file"
            file "$file"
            ls -l "$file"
            echo "MIME type: $(file -i $file)"
        else
            echo "✗ Arquivo não encontrado: $file"
        fi
    done
}

echo "=== Iniciando processo de build ==="

echo "1. Instalando dependências Python..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "2. Instalando dependências Node.js..."
npm install

echo "3. Verificando configuração do Tailwind..."
if [ -f "tailwind.config.js" ]; then
    echo "✓ Configuração do Tailwind encontrada"
    echo "3.1. Construindo CSS com Tailwind..."
    npm run build
else
    echo "✗ Configuração do Tailwind não encontrada, pulando build"
fi

echo "4. Limpando diretório de arquivos estáticos..."
rm -rf staticfiles/*

echo "5. Verificando arquivos estáticos de origem..."
echo "5.1. Verificando arquivos CSS..."
check_files "static/css" "*.css"

echo "5.2. Verificando arquivos JavaScript..."
check_files "static/js" "*.js"

echo "5.3. Verificando imagens..."
check_files "static/images" "*"

echo "6. Coletando arquivos estáticos..."
python manage.py collectstatic --no-input -v 3

echo "7. Verificando arquivos coletados..."
echo "7.1. Verificando CSS coletados..."
check_files "staticfiles/css" "*.css"

echo "7.2. Verificando JavaScript coletados..."
check_files "staticfiles/js" "*.js"

echo "7.3. Verificando imagens coletadas..."
check_files "staticfiles/images" "*"

echo "7.4. Verificando arquivos admin..."
if [ -d "staticfiles/admin" ]; then
    echo "✓ Arquivos admin coletados com sucesso"
    ls -la staticfiles/admin/
else
    echo "✗ Arquivos admin não encontrados"
    exit 1
fi

echo "8. Verificando permissões..."
find staticfiles -type d -exec chmod 755 {} \;
find staticfiles -type f -exec chmod 644 {} \;

echo "9. Verificando manifesto do WhiteNoise..."
if [ -f "staticfiles/staticfiles.json" ]; then
    echo "✓ Manifesto do WhiteNoise gerado com sucesso"
    cat staticfiles/staticfiles.json
else
    echo "✗ Manifesto do WhiteNoise não encontrado"
    exit 1
fi

echo "10. Executando migrações do banco de dados..."
python manage.py migrate

echo "11. Verificando configuração WSGI..."
if [ -f "hoztechsite/wsgi.py" ]; then
    echo "✓ Arquivo WSGI encontrado"
else
    echo "✗ Arquivo WSGI não encontrado"
    exit 1
fi

# Criar superusuário se ADMIN_PASSWORD estiver definido
if [[ -n "${ADMIN_PASSWORD}" ]]; then
    echo "12. Criando superusuário..."
    python manage.py createsuperuser --noinput --username admin \
        --email admin@example.com
fi

echo "=== Build concluído com sucesso ==="

# Exibir informações de debug
echo "=== Informações de Debug ==="
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"
echo "Diretório atual: $(pwd)"
echo "Conteúdo do diretório staticfiles:"
ls -la staticfiles/
echo "Verificando MIME types dos arquivos CSS:"
file -i staticfiles/css/*
echo "Verificando MIME types dos arquivos JS:"
file -i staticfiles/js/*
echo "=== Fim das informações de Debug ===" 