from PIL import Image
import os

def optimize_image(input_path, output_path, max_size_kb=200):
    # Abrir a imagem
    img = Image.open(input_path)
    
    # Preservar o modo de cor
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        # Converter para RGBA se tiver transparência
        img = img.convert('RGBA')
    else:
        # Caso contrário, converter para RGB
        img = img.convert('RGB')
    
    # Calcular dimensões mantendo proporção
    max_dimension = 800  # Tamanho máximo para qualquer dimensão
    ratio = min(max_dimension/float(img.size[0]), max_dimension/float(img.size[1]))
    new_size = tuple([int(x*ratio) for x in img.size])
    
    # Redimensionar usando LANCZOS (alta qualidade)
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    
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

    return size_kb, quality

if __name__ == '__main__':
    input_file = 'static/images/logo.png'
    output_file = 'static/images/logo_optimized.png'
    
    # Fazer backup do arquivo original
    import shutil
    backup_file = 'static/images/logo_original.png'
    shutil.copy2(input_file, backup_file)
    
    # Otimizar
    size_kb, quality = optimize_image(input_file, output_file)
    
    # Substituir arquivo original com versão otimizada
    os.replace(output_file, input_file)
    
    print(f'Imagem otimizada com sucesso!')
    print(f'Qualidade final: {quality}%')
    print(f'Tamanho final: {size_kb:.2f}KB')
    print(f'Backup do arquivo original salvo como: {backup_file}') 