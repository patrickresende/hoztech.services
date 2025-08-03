#!/usr/bin/env python3
"""
Script para limpar configurações HSTS e garantir acesso HTTP em desenvolvimento
"""

import os
import sys
import webbrowser
import time

def clear_hsts_instructions():
    """Mostra instruções para limpar HSTS em diferentes navegadores"""
    
    print("=" * 60)
    print("🔧 SOLUÇÕES PARA REDIRECIONAMENTO HTTPS FORÇADO")
    print("=" * 60)
    
    print("\n1️⃣ CHROME/EDGE:")
    print("   • Digite na barra de endereços: chrome://net-internals/#hsts")
    print("   • Na seção 'Delete domain security policies':")
    print("   • Digite: 127.0.0.1")
    print("   • Clique em 'Delete'")
    print("   • Digite: localhost")
    print("   • Clique em 'Delete'")
    
    print("\n2️⃣ FIREFOX:")
    print("   • Digite na barra de endereços: about:preferences#privacy")
    print("   • Role até 'Cookies e dados do site'")
    print("   • Clique em 'Limpar dados...'")
    print("   • Marque 'Cookies e dados do site'")
    print("   • Clique em 'Limpar'")
    
    print("\n3️⃣ SOLUÇÃO RÁPIDA:")
    print("   • Use uma aba INCÓGNITA/PRIVADA")
    print("   • Ou limpe todo o cache do navegador (Ctrl+Shift+Delete)")
    
    print("\n4️⃣ ALTERNATIVA:")
    print("   • Tente usar: http://localhost:8000/")
    print("   • Em vez de: http://127.0.0.1:8000/")
    
    print("\n" + "=" * 60)
    print("🌐 URLs CORRETAS PARA DESENVOLVIMENTO:")
    print("=" * 60)
    print("✅ http://127.0.0.1:8000/")
    print("✅ http://localhost:8000/")
    print("❌ https://127.0.0.1:8000/ (NÃO USE)")
    print("❌ https://localhost:8000/ (NÃO USE)")
    
    return True

def open_browser_with_http():
    """Tenta abrir o navegador com HTTP forçado"""
    
    urls_to_try = [
        "http://127.0.0.1:8000/",
        "http://localhost:8000/"
    ]
    
    print("\n🚀 Tentando abrir o site no navegador...")
    
    for url in urls_to_try:
        try:
            print(f"   Tentando: {url}")
            webbrowser.open(url)
            time.sleep(2)
            break
        except Exception as e:
            print(f"   Erro ao abrir {url}: {e}")
            continue
    
    return True

def main():
    """Função principal"""
    
    print("🔧 Limpador de HSTS - HOZ TECH")
    print("Este script ajuda a resolver redirecionamentos HTTPS forçados\n")
    
    # Mostrar instruções
    clear_hsts_instructions()
    
    # Perguntar se quer abrir o navegador
    try:
        choice = input("\n🌐 Deseja tentar abrir o site no navegador? (s/n): ").lower().strip()
        if choice in ['s', 'sim', 'y', 'yes']:
            open_browser_with_http()
    except KeyboardInterrupt:
        print("\n\n👋 Script cancelado pelo usuário.")
        return
    
    print("\n✅ Script concluído!")
    print("💡 Se ainda houver problemas, siga as instruções acima para limpar o HSTS.")

if __name__ == "__main__":
    main()