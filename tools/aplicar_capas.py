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

def encontrar_imagens_produto(pasta_produto, capa_base):
    """Encontra todas as imagens do produto, priorizando a capa definida"""
    imagens = []
    encontrou_capa = False
    
    # Se não há capa definida, retorna vazio para tratamento posterior
    if capa_base is None:
        return []
    
    # Procura a imagem de capa primeiro
    for entry in os.scandir(pasta_produto):
        if not entry.is_file():
            continue
        
        nome, ext = os.path.splitext(entry.name)
        if ext.lower() not in IMAGE_EXTS:
            continue
            
        if nome == capa_base:
            encontrou_capa = True
            
            # Cria caminhos para imagens desktop e mobile
            desktop_path = os.path.join(pasta_produto, f"{nome}-desktop.webp")
            mobile_path = os.path.join(pasta_produto, f"{nome}-mobile.webp")
            full_path = entry.path
            
            # Verifica se as versões redimensionadas existem
            desktop_exists = os.path.exists(desktop_path)
            mobile_exists = os.path.exists(mobile_path)
            
            # Usa os caminhos relativos para o objeto productImagesByCode
            rel_desktop = os.path.relpath(desktop_path if desktop_exists else full_path, FOTOS_DIR).replace("\\", "/")
            rel_mobile = os.path.relpath(mobile_path if mobile_exists else full_path, FOTOS_DIR).replace("\\", "/")
            rel_full = os.path.relpath(full_path, FOTOS_DIR).replace("\\", "/")
            
            imagens.append({
                "desktop": rel_desktop,
                "mobile": rel_mobile,
                "full": rel_full
            })
            break
    
    # Se não encontrou a capa, tenta usar qualquer imagem disponível
    if not encontrou_capa:
        for entry in os.scandir(pasta_produto):
            if not entry.is_file():
                continue
            
            nome, ext = os.path.splitext(entry.name)
            if ext.lower() not in IMAGE_EXTS:
                continue
                
            # Ignora derivados (desktop/mobile)
            if nome.endswith("-desktop") or nome.endswith("-mobile"):
                continue
                
            # Usa essa imagem como alternativa
            desktop_path = os.path.join(pasta_produto, f"{nome}-desktop.webp")
            mobile_path = os.path.join(pasta_produto, f"{nome}-mobile.webp")
            full_path = entry.path
            
            desktop_exists = os.path.exists(desktop_path)
            mobile_exists = os.path.exists(mobile_path)
            
            rel_desktop = os.path.relpath(desktop_path if desktop_exists else full_path, FOTOS_DIR).replace("\\", "/")
            rel_mobile = os.path.relpath(mobile_path if mobile_exists else full_path, FOTOS_DIR).replace("\\", "/")
            rel_full = os.path.relpath(full_path, FOTOS_DIR).replace("\\", "/")
            
            imagens.append({
                "desktop": rel_desktop,
                "mobile": rel_mobile,
                "full": rel_full
            })
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
