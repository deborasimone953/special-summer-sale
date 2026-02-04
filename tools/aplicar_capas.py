#!/usr/bin/env python3
import json
import os
import re

# Diretórios do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")
COVER_FILE_NAME = ".capa.txt"

# Extensões de imagens válidas
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"]

def obter_codigo_produto(nome_pasta):
    """Extrai o código do produto do nome da pasta"""
    if " - " in nome_pasta:
        codigo = nome_pasta.split(" - ", 1)[0].strip()
        if codigo:
            return codigo
    # Caso especial para produtos com código PROD-XXXX
    if nome_pasta.startswith('PROD-'):
        match = re.search(r'(PROD-[0-9]+)\s*-', nome_pasta)
        if match:
            return match.group(1).strip()
    
    # Caso normal para outros formatos de código
    match = re.search(r'([A-Z0-9]+)\s*-', nome_pasta)
    if match:
        return match.group(1).strip()
    
    return None

def ler_capa_produto(pasta_produto):
    """Lê o arquivo de capa de um produto e retorna o nome base da imagem"""
    cover_path = os.path.join(pasta_produto, COVER_FILE_NAME)
    if not os.path.exists(cover_path):
        return None
    
    with open(cover_path, "r", encoding="utf-8") as handle:
        conteudo = handle.read().strip()
    
    return conteudo if conteudo else None

def _build_image_entry(pasta_produto, base_name):
    full_path = None
    for ext in IMAGE_EXTS:
        candidate = os.path.join(pasta_produto, f"{base_name}{ext}")
        if os.path.exists(candidate):
            full_path = candidate
            break

    desktop_path = os.path.join(pasta_produto, f"{base_name}-desktop.webp")
    mobile_path = os.path.join(pasta_produto, f"{base_name}-mobile.webp")

    desktop_exists = os.path.exists(desktop_path)
    mobile_exists = os.path.exists(mobile_path)

    if not full_path:
        if desktop_exists:
            full_path = desktop_path
        elif mobile_exists:
            full_path = mobile_path

    if not full_path and not desktop_exists and not mobile_exists:
        return None

    rel_desktop = os.path.relpath(desktop_path if desktop_exists else full_path, FOTOS_DIR).replace("\\", "/")
    rel_mobile = os.path.relpath(mobile_path if mobile_exists else full_path, FOTOS_DIR).replace("\\", "/")
    rel_full = os.path.relpath(full_path, FOTOS_DIR).replace("\\", "/")

    return {
        "desktop": f"assets/fotos/{rel_desktop}",
        "mobile": f"assets/fotos/{rel_mobile}",
        "full": f"assets/fotos/{rel_full}",
    }

def encontrar_imagens_produto(pasta_produto, capa_base):
    """Encontra todas as imagens do produto, priorizando a capa definida"""
    imagens = []

    # Se não há capa definida, retorna vazio para tratamento posterior
    if capa_base is None:
        return []

    for base_name in (capa_base, f"capa {capa_base}"):
        entry = _build_image_entry(pasta_produto, base_name)
        if entry:
            imagens.append(entry)
            return imagens

    # Se não encontrou a capa, tenta usar qualquer imagem disponível
    for entry in os.scandir(pasta_produto):
        if not entry.is_file():
            continue

        nome, ext = os.path.splitext(entry.name)
        if ext.lower() not in IMAGE_EXTS:
            continue

        # Ignora derivados (desktop/mobile)
        if nome.endswith("-desktop") or nome.endswith("-mobile"):
            continue

        image_entry = _build_image_entry(pasta_produto, nome)
        if image_entry:
            imagens.append(image_entry)
            break
    
    return imagens

def gerar_mapeamento_imagens():
    """Gera o objeto productImagesByCode com base nas capas definidas"""
    mapeamento = {}
    
    # Percorre todas as categorias
    for categoria in os.listdir(FOTOS_DIR):
        categoria_path = os.path.join(FOTOS_DIR, categoria)
        if not os.path.isdir(categoria_path):
            continue
            
        # Percorre todos os produtos da categoria
        for produto in os.listdir(categoria_path):
            produto_path = os.path.join(categoria_path, produto)
            if not os.path.isdir(produto_path):
                continue
                
            # Extrai o código do produto
            codigo = obter_codigo_produto(produto)
            if not codigo:
                print(f"Não foi possível obter código do produto: {produto}")
                continue
                
            # Lê a imagem de capa do produto
            capa_base = ler_capa_produto(produto_path)
            
            # Encontra as imagens do produto
            imagens = encontrar_imagens_produto(produto_path, capa_base)
            
            # Se encontrou imagens, adiciona ao mapeamento
            if imagens:
                mapeamento[codigo] = imagens
    
    return mapeamento

def gerar_js_atualizado():
    """Gera o código JavaScript atualizado com as novas capas"""
    mapeamento = gerar_mapeamento_imagens()
    
    # Converte o objeto Python para formato JavaScript
    js_object = json.dumps(mapeamento, indent=2)
    
    # Formata o código para o formato esperado em JavaScript
    js_code = js_object.replace('"desktop":', 'desktop:').replace('"mobile":', 'mobile:').replace('"full":', 'full:')
    
    # Gera o arquivo JavaScript completo
    script_completo = f"""// Script gerado automaticamente pela ferramenta aplicar_capas.py
// Este script atualiza as imagens de capa dos produtos selecionadas pela ferramenta selecionar_capa.py

window.addEventListener('DOMContentLoaded', function() {{
  console.log("Aplicando imagens de capa atualizadas...");
  
  // Definição do objeto productImagesByCode com as capas atualizadas
  window.productImagesByCode = {js_code};
  
  // Aplicar as imagens após um pequeno atraso
  setTimeout(function() {{
    if (typeof window.applyProductImages === 'function') {{
      console.log('Aplicando imagens aos produtos...');
      window.applyProductImages();
      
      // Verificação para garantir que as imagens foram aplicadas
      setTimeout(function() {{
        console.log('Verificando aplicação de imagens...');
        window.applyProductImages();
        console.log('Produtos disponíveis:', Object.keys(window.productImagesByCode).length);
      }}, 500);
    }} else {{
      console.error('Função applyProductImages não encontrada!');
    }}
  }}, 200);
}});
"""
    
    return script_completo

def salvar_script_atualizado(conteudo):
    """Salva o script JavaScript atualizado"""
    arquivo_saida = os.path.join(BASE_DIR, "atualizar_capas.js")
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return arquivo_saida

def main():
    print("Iniciando atualização de capas de produtos...")
    
    # Gera o conteúdo do script atualizado
    js_atualizado = gerar_js_atualizado()
    
    # Salva o script
    caminho_script = salvar_script_atualizado(js_atualizado)
    
    print(f"Script gerado com sucesso: {caminho_script}")
    print("")
    print("Para aplicar as novas capas no site, adicione este script no arquivo index.html:")
    print("<script src=\"atualizar_capas.js\"></script>")
    print("")
    print("Ou substitua a referência existente para qualquer outro script de imagens.")

if __name__ == "__main__":
    main()
