#!/usr/bin/env bash
set -o errexit

# Função utilitária para verificar arquivos
check_files() {
    local dir=$1
    local pattern=$2

    echo "📂 Verificando arquivos em $dir com padrão $pattern"
    if [ ! -d "$dir" ]; then
        echo "✗ Diretório não encontrado: $dir"
        return
    fi

    local found=false
    for file in $dir/$pattern; do
        if [ -f "$file" ]; then
            echo "✓ Arquivo: $file"
            file "$file"
            ls -l "$file"
            echo "MIME type: $(file -i "$file")"
            found=true
        fi
    done

    if [ "$found" = false ]; then
        echo "✗ Nenhum arquivo encontrado em $dir com padrão $pattern"
    fi
}

instalar_dependencias() {
    echo "1. Instalando dependências Python e Node..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    npm install
}

compilar_tailwind() {
    echo "2. Verificando configuração do Tailwind..."
    if [ -f "tailwind.config.js" ]; then
        echo "✓ Tailwind configurado. Compilando..."
        npm run build
    else
        echo "✗ Tailwind não configurado. Pulando..."
    fi
}

verificar_arquivos_origem() {
    echo "3. Verificando arquivos estáticos de origem..."
    check_files "static/css" "*.css"
    check_files "static/js" "*.js"
    check_files "static/images" "*"
}

coletar_staticfiles() {
    echo "4. Limpando e coletando arquivos estáticos..."
    rm -rf staticfiles/*
    python manage.py collectstatic --no-input -v 3
}

verificar_staticfiles() {
    echo "5. Verificando arquivos coletados..."
    check_files "staticfiles/css" "*.css"
    check_files "staticfiles/js" "*.js"
    check_files "staticfiles/images" "*"

    echo "5.4. Verificando admin..."
    if [ -d "staticfiles/admin" ]; then
        echo "✓ Arquivos admin coletados"
        ls -la staticfiles/admin/
    else
        echo "✗ Arquivos admin não encontrados"
        exit 1
    fi
}

ajustar_permissoes() {
    echo "6. Ajustando permissões de arquivos..."
    find staticfiles -type d -exec chmod 755 {} \;
    find staticfiles -type f -exec chmod 644 {} \;
}

verificar_manifesto() {
    echo "7. Verificando manifesto do WhiteNoise..."
    if [ -f "staticfiles/staticfiles.json" ]; then
        echo "✓ Manifesto encontrado:"
        cat staticfiles/staticfiles.json
    else
        echo "✗ Manifesto não encontrado"
        exit 1
    fi
}

executar_migracoes() {
    echo "8. Executando migrações..."
    python manage.py migrate
}

verificar_wsgi() {
    echo "9. Verificando WSGI..."
    if [ -f "hoztechsite/wsgi.py" ]; then
        echo "✓ WSGI presente"
    else
        echo "✗ Arquivo WSGI ausente"
        exit 1
    fi
}

criar_superusuario() {
    if [[ -n "${ADMIN_PASSWORD}" ]]; then
        echo "10. Criando superusuário..."
        python manage.py createsuperuser --noinput --username admin \
            --email admin@example.com
    fi
}

exibir_debug() {
    echo "=== Informações de Debug ==="
    echo "Python: $(python --version)"
    echo "Pip: $(pip --version)"
    echo "Node: $(node --version)"
    echo "NPM: $(npm --version)"
    echo "Diretório atual: $(pwd)"
    echo "Conteúdo do staticfiles:"
    ls -la staticfiles/

    echo "MIME types CSS:"
    file -i staticfiles/css/* || true

    echo "MIME types JS:"
    file -i staticfiles/js/* || true

    echo "=== Fim do Debug ==="
}

# Execução
echo "=== Iniciando processo de build ==="

instalar_dependencias
compilar_tailwind
verificar_arquivos_origem
coletar_staticfiles
verificar_staticfiles
ajustar_permissoes
verificar_manifesto
executar_migracoes
verificar_wsgi
criar_superusuario
exibir_debug

echo "=== ✅ Build concluído com sucesso ==="
