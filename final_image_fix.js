// Script final para correção de imagens baseado na versão que funciona (direct_fix.html)
document.addEventListener('DOMContentLoaded', function() {
  console.log('Aplicando correção final de imagens...');
  
  // Mapeamento de produtos para imagens externas
  const imagemPorCodigo = {
    "VMSF01": "https://varandamix.com/wp-content/uploads/2024/01/sofa-organico-700x700.webp",
    "VMSF02": "https://varandamix.com/wp-content/uploads/2024/01/sofa-meridiano-700x700.webp",
    "VMSF03": "https://varandamix.com/wp-content/uploads/2024/01/sofa-oak-700x700.webp",
    "VMSF04": "https://varandamix.com/wp-content/uploads/2024/01/sofa-latt-700x700.webp",
    "EX01": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-flam-700x700.webp",
    "EX02": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-bonina-700x700.webp",
    "EX03": "https://varandamix.com/wp-content/uploads/2024/01/mesa-lateral-rueda-700x700.webp",
    "EX04": "https://varandamix.com/wp-content/uploads/2024/01/tapete-ara-700x700.webp",
    "EX05": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-soho-700x700.webp",
    "EX06": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-fiji-700x700.webp",
    "EX07": "https://varandamix.com/wp-content/uploads/2023/12/balanco-luar-700x700.webp",
    "EX08": "https://varandamix.com/wp-content/uploads/2023/12/balanco-suporte-700x700.webp",
    "EX09": "https://varandamix.com/wp-content/uploads/2023/12/espreguicadeira-700x700.webp",
    "EX010": "https://varandamix.com/wp-content/uploads/2023/12/sofa-externo-700x700.webp",
    
    // Adicionar versões com hífen para compatibilidade
    "EX-01": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-flam-700x700.webp",
    "EX-02": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-bonina-700x700.webp",
    "EX-03": "https://varandamix.com/wp-content/uploads/2024/01/mesa-lateral-rueda-700x700.webp",
    "EX-04": "https://varandamix.com/wp-content/uploads/2024/01/tapete-ara-700x700.webp",
    "EX-05": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-soho-700x700.webp",
    "EX-06": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-fiji-700x700.webp",
    "EX-07": "https://varandamix.com/wp-content/uploads/2023/12/balanco-luar-700x700.webp",
    "EX-08": "https://varandamix.com/wp-content/uploads/2023/12/balanco-suporte-700x700.webp",
    "EX-09": "https://varandamix.com/wp-content/uploads/2023/12/espreguicadeira-700x700.webp",
    "EX-010": "https://varandamix.com/wp-content/uploads/2023/12/sofa-externo-700x700.webp",
    
    "VMSF-01": "https://varandamix.com/wp-content/uploads/2024/01/sofa-organico-700x700.webp",
    "VMSF-02": "https://varandamix.com/wp-content/uploads/2024/01/sofa-meridiano-700x700.webp",
    "VMSF-03": "https://varandamix.com/wp-content/uploads/2024/01/sofa-oak-700x700.webp",
    "VMSF-04": "https://varandamix.com/wp-content/uploads/2024/01/sofa-latt-700x700.webp"
  };
  
  // Imagem genérica para produtos sem correspondência
  const imagemGenerica = "https://varandamix.com/wp-content/uploads/2023/12/produto-generico-700x700.webp";
  
  // Função para criar o HTML do slide
  function createSlideHTML(imageUrl, altText) {
    return '<div class="swiper-slide"><img src="' + imageUrl + '" alt="' + altText + '" loading="lazy" style="width: 100%; height: auto;"></div>';
  }
  
  // Encontrar todos os slides de produtos
  const slides = document.querySelectorAll('.product-swiper-wrapper .swiper-slide');
  console.log(`Encontrados ${slides.length} slides de produtos`);
  
  // Contador para acompanhamento
  let slidesTratados = 0;
  let slidesComImagem = 0;
  
  // Aplicar imagens a cada slide
  slides.forEach(function(slide) {
    slidesTratados++;
    
    // Encontrar o código do produto
    const codeElement = slide.querySelector('.product-code');
    if (!codeElement) {
      console.log(`Slide #${slidesTratados} não tem código de produto`);
      return;
    }
    
    const codigo = codeElement.textContent.trim();
    console.log(`Processando produto #${slidesTratados}: ${codigo}`);
    
    // Encontrar o nome do produto (para texto alternativo)
    const nomeElement = slide.querySelector('h6');
    const nomeProduto = nomeElement ? nomeElement.textContent.trim() : 'Produto';
    
    // Encontrar o wrapper de imagens
    const wrapper = slide.querySelector('.product-images .swiper-wrapper');
    if (!wrapper) {
      console.log(`Wrapper de imagens não encontrado para ${codigo}`);
      return;
    }
    
    // Obter URL da imagem do mapeamento ou usar genérica
    const imageUrl = imagemPorCodigo[codigo] || imagemGenerica;
    
    // Inserir a imagem no slide
    wrapper.innerHTML = createSlideHTML(imageUrl, nomeProduto);
    console.log(`Imagem aplicada para ${codigo}`);
    slidesComImagem++;
  });
  
  console.log(`Processamento concluído: ${slidesTratados} slides processados, ${slidesComImagem} com imagens aplicadas`);
});
