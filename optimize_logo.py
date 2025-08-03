import os
import sys
import shutil
from PIL import Image, ImageOps

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        from PIL import Image
        return True
    except ImportError:
        print("❌ Erro: Pillow não está instalado!")
        print("📦 Instale com: pip install Pillow")
        return False

def optimize_image(input_path, output_path, max_size_kb=200, max_dimension=800):
    """Otimiza imagem mantendo qualidade e transparência"""
    
    if not check_dependencies():
        return False, 0, 0
    
    try:
        print(f"📁 Processando: {input_path}")
        
        # Abrir a imagem
        img = Image.open(input_path)
        original_size = img.size
        original_format = img.format
        
        print(f"📏 Tamanho original: {original_size[0]}x{original_size[1]} pixels")
        
        # Preservar o modo de cor
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Converter para RGBA se tiver transparência
            img = img.convert('RGBA')
            print("🎨 Modo: RGBA (com transparência)")
        else:
            # Caso contrário, converter para RGB
            img = img.convert('RGB')
            print("🎨 Modo: RGB")
        
        # Calcular dimensões mantendo proporção
        ratio = min(max_dimension/float(img.size[0]), max_dimension/float(img.size[1]))
        new_size = tuple([int(x*ratio) for x in img.size])
        
        if new_size != original_size:
            print(f"📐 Redimensionando para: {new_size[0]}x{new_size[1]} pixels")
            # Redimensionar usando LANCZOS (alta qualidade)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        else:
            print("📐 Mantendo tamanho original")
        
        # Salvar com otimização
        quality = 95
        while quality > 50:  # Não reduzir qualidade abaixo de 50
            if img.mode == 'RGBA':
                # Para PNG com transparência
                img.save(output_path, 'PNG', optimize=True, quality=quality)
            else:
                # Para JPEG sem transparência
                img.save(output_path, 'JPEG', optimize=True, quality=quality)
            
            # Verificar tamanho
            size_kb = os.path.getsize(output_path) / 1024
            if size_kb <= max_size_kb:
                break
                
            quality -= 5
        
        return True, size_kb, quality
        
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
        return False, 0, 0

def create_backup(input_path, backup_dir="backups"):
    """Cria backup do arquivo original"""
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        filename = os.path.basename(input_path)
        backup_path = os.path.join(backup_dir, f"original_{filename}")
        shutil.copy2(input_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"⚠️  Erro ao criar backup: {e}")
        return None

def main():
    """Função principal"""
    print("🖼️  Otimizador de Imagens HOZ TECH")
    print("=" * 50)
    
    # Configurações via variáveis de ambiente
    input_file = os.getenv('OPTIMIZE_INPUT', 'core/static/core/images/logo.png')
    max_size_kb = int(os.getenv('OPTIMIZE_MAX_SIZE', '200'))
    max_dimension = int(os.getenv('OPTIMIZE_MAX_DIMENSION', '800'))
    create_backup_flag = os.getenv('OPTIMIZE_BACKUP', 'true').lower() == 'true'
    
    # Verificar se arquivo existe
    if not os.path.exists(input_file):
        print(f"❌ Arquivo não encontrado: {input_file}")
        print("💡 Verifique o caminho ou defina OPTIMIZE_INPUT")
        sys.exit(1)
    
    # Criar backup se solicitado
    backup_path = None
    if create_backup_flag:
        print("💾 Criando backup...")
        backup_path = create_backup(input_file)
        if backup_path:
            print(f"✅ Backup criado: {backup_path}")
    
    # Arquivo temporário para otimização
    output_file = input_file + '.optimized'
    
    # Otimizar imagem
    success, size_kb, quality = optimize_image(input_file, output_file, max_size_kb, max_dimension)
    
    if success:
        # Substituir arquivo original com versão otimizada
        os.replace(output_file, input_file)
        
        print("✅ Otimização concluída com sucesso!")
        print(f"📊 Qualidade final: {quality}%")
        print(f"📏 Tamanho final: {size_kb:.2f}KB")
        if backup_path:
            print(f"💾 Backup salvo em: {backup_path}")
        
        # Mostrar economia
        original_size = os.path.getsize(backup_path) / 1024 if backup_path else 0
        if original_size > 0:
            savings = ((original_size - size_kb) / original_size) * 100
            print(f"💰 Economia: {savings:.1f}%")
    else:
        print("❌ Falha na otimização!")
        if os.path.exists(output_file):
            os.remove(output_file)
        sys.exit(1)

if __name__ == '__main__':
    main() 