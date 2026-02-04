#!/usr/bin/env python3
import os
import re
import json

# Diretórios do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")
OUTPUT_FILE = os.path.join(BASE_DIR, "direct_capas.js")

# Extensões de imagens válidas
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"]

def obter_codigo_produto(nome_pasta):
    """Extrai o código do produto do nome da pasta"""
    # Caso especial para produtos com código PROD-XXXX
    if nome_pasta.startswith('PROD-'):
        match = re.search(r'(PROD-[0-9]+)', nome_pasta)
        if match:
            return match.group(1).strip()
    
    # Casos especiais para outros formatos com hífen
    match = re.search(r'([A-Z0-9]+-[0-9]+)', nome_pasta)
    if match:
        return match.group(1).strip()
    
    # Caso normal para outros formatos de código
    match = re.search(r'([A-Z0-9]+)', nome_pasta)
    if match:
        return match.group(1).strip()
    
    return None

def encontrar_melhor_imagem(pasta_produto):
    """Encontra a melhor imagem para usar como capa"""
    imagens = []
    
    # Procurar todas as imagens na pasta
    for item in os.listdir(pasta_produto):
        caminho_completo = os.path.join(pasta_produto, item)
        if os.path.isfile(caminho_completo):
            nome, ext = os.path.splitext(item)
            if ext.lower() in IMAGE_EXTS and not nome.endswith('-desktop') and not nome.endswith('-mobile'):
                # Prioriza imagens com nomes específicos
                prioridade = 0
                if item.lower() == 'capa.jpg' or item.lower() == 'capa.png':
                    prioridade = 10
                elif nome.lower().startswith('capa'):
                    prioridade = 9
                elif nome.endswith('-01') or nome.endswith('-1'):
                    prioridade = 8
                elif nome.endswith('-02') or nome.endswith('-2'):
                    prioridade = 7
                elif nome.endswith('-03') or nome.endswith('-3'):
                    prioridade = 6
                
                # Verifica se tem versões desktop e mobile
                desktop_exists = os.path.exists(os.path.join(pasta_produto, f"{nome}-desktop.webp"))
                mobile_exists = os.path.exists(os.path.join(pasta_produto, f"{nome}-mobile.webp"))
                
                # Prioriza imagens que têm versões otimizadas
                if desktop_exists and mobile_exists:
                    prioridade += 3
                
                imagens.append((prioridade, item, desktop_exists, mobile_exists))
    
    # Se não encontrou nenhuma imagem
    if not imagens:
        return None
    
    # Ordena por prioridade e pega a melhor imagem
    imagens.sort(reverse=True)
    return imagens[0]

def gerar_js_atualizado():
    """Gera o código JavaScript atualizado com as novas capas"""
    mapeamento = {}
    produtos_sem_imagem = []
    
    # Diretório "Sem categoria"
    categoria_path = os.path.join(FOTOS_DIR, "Sem categoria")
    
    # Percorre todas as pastas de produto
    for item in os.listdir(categoria_path):
        produto_path = os.path.join(categoria_path, item)
        if os.path.isdir(produto_path):
            codigo = obter_codigo_produto(item)
            
            if codigo:
                # Encontra a melhor imagem para o produto
                melhor_imagem = encontrar_melhor_imagem(produto_path)
                
                if melhor_imagem:
                    prioridade, nome_arquivo, desktop_exists, mobile_exists = melhor_imagem
                    nome_base, ext = os.path.splitext(nome_arquivo)
                    
                    # Define caminhos relativos
                    caminho_completo = os.path.join(produto_path, nome_arquivo)
                    caminho_desktop = os.path.join(produto_path, f"{nome_base}-desktop.webp")
                    caminho_mobile = os.path.join(produto_path, f"{nome_base}-mobile.webp")
                    
                    rel_desktop = os.path.relpath(
                        caminho_desktop if desktop_exists else caminho_completo,
                        FOTOS_DIR,
                    ).replace("\\", "/")
                    rel_mobile = os.path.relpath(
                        caminho_mobile if mobile_exists else caminho_completo,
                        FOTOS_DIR,
                    ).replace("\\", "/")
                    rel_full = os.path.relpath(caminho_completo, FOTOS_DIR).replace("\\", "/")

                    rel_desktop = f"assets/fotos/{rel_desktop}"
                    rel_mobile = f"assets/fotos/{rel_mobile}"
                    rel_full = f"assets/fotos/{rel_full}"
                    
                    mapeamento[codigo] = [
                        {
                            "desktop": rel_desktop,
                            "mobile": rel_mobile,
                            "full": rel_full
                        }
                    ]
                else:
                    produtos_sem_imagem.append((codigo, item))
            else:
                produtos_sem_imagem.append(("código não encontrado", item))
    
    # Converte o objeto Python para formato JavaScript
    js_object = json.dumps(mapeamento, indent=2)
    
    # Formata o código para o formato esperado em JavaScript
    js_code = js_object.replace('"desktop":', 'desktop:').replace('"mobile":', 'mobile:').replace('"full":', 'full:')
    
    # Adiciona informações de depuração ao final do arquivo
    debug_info = []
    debug_info.append(f"// Total de produtos encontrados: {len(mapeamento)}")
    if produtos_sem_imagem:
        debug_info.append(f"// Produtos sem imagem: {len(produtos_sem_imagem)}")
        for codigo, nome in produtos_sem_imagem:
            debug_info.append(f"// - {codigo}: {nome}")
    
    debug_text = "\n".join(debug_info)
    
    # Gera o arquivo JavaScript completo
    script_completo = f"""// Script gerado automaticamente pela ferramenta direct_image_updater.py
// Este script define diretamente as imagens de capa para todos os produtos

window.addEventListener('DOMContentLoaded', function() {{
  console.log("Aplicando imagens de capa diretas...");
  
  // Definição do objeto productImagesByCode com as capas
  window.productImagesByCode = {js_code};
  
  // Aplicar as imagens imediatamente
  setTimeout(function() {{
    if (typeof window.applyProductImages === 'function') {{
      console.log('Aplicando imagens aos produtos...');
      window.applyProductImages();
      
      // Verificação para garantir que as imagens foram aplicadas
      setTimeout(function() {{
        console.log('Verificando aplicação de imagens...');
        window.applyProductImages();
        console.log('Produtos disponíveis:', Object.keys(window.productImagesByCode).length);
      }}, 1000);
    }} else {{
      console.error('Função applyProductImages não encontrada!');
      
      // Define uma função applyProductImages caso não exista
      window.applyProductImages = function() {{
        document.querySelectorAll('.product-swiper-wrapper .swiper-slide').forEach((slide) => {{
          const codeElement = slide.querySelector('.product-code');
          if (!codeElement) return;
          
          const code = codeElement.textContent.trim();
          if (!code) return;
          
          const images = window.productImagesByCode[code] || window.productImagesByCode[code.replace(/\\s+/g, '')];
          
          if (!images || !images.length) return;
          
          const wrapper = slide.querySelector('.product-images .swiper-wrapper');
          if (!wrapper) return;
          
          wrapper.innerHTML = images.map(img => 
            `<div class="swiper-slide"><img src="${{img.desktop}}" srcset="${{img.desktop}} 1x, ${{img.full}} 2x" loading="lazy" alt=""></div>`
          ).join('');
        }});
      }};
      
      // Aplica as imagens
      window.applyProductImages();
    }}
  }}, 100);
}});

{debug_text}
"""
    
    return script_completo

def main():
    print("Iniciando varredura de pastas para encontrar imagens...")
    
    # Gera o conteúdo do script atualizado
    js_atualizado = gerar_js_atualizado()
    
    # Salva o script
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_atualizado)
    
    print(f"Script gerado com sucesso: {OUTPUT_FILE}")
    print("")
    print("Para aplicar as novas capas no site, adicione este script no arquivo index.html:")
    print("<script src=\"direct_capas.js\"></script>")
    print("")

if __name__ == "__main__":
    main()
