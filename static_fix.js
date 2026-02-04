// Script para adicionar imagens estáticas para os slides principais
document.addEventListener('DOMContentLoaded', function() {
  console.log('Aplicando correção estática de imagens...');
  
  // Mapeamento de produtos para imagens estáticas (URLs absolutas)
  const imagensEstaticas = {
    "VMSF01": "https://varandamix.com/wp-content/uploads/2024/01/sofa-organico-700x700.webp",
    "VMSF02": "https://varandamix.com/wp-content/uploads/2024/01/sofa-meridiano-700x700.webp",
    "VMSF03": "https://varandamix.com/wp-content/uploads/2024/01/sofa-oak-700x700.webp",
    "VMSF04": "https://varandamix.com/wp-content/uploads/2024/01/sofa-latt-700x700.webp",
    "EX01": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-flam-700x700.webp",
    "EX02": "https://varandamix.com/wp-content/uploads/2024/01/poltrona-bonina-700x700.webp",
    "EX03": "https://varandamix.com/wp-content/uploads/2024/01/mesa-lateral-rueda-700x700.webp",
    "EX04": "https://varandamix.com/wp-content/uploads/2024/01/tapete-ara-700x700.webp",
    "EX05": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-soho-700x700.webp",
    "EX06": "https://varandamix.com/wp-content/uploads/2024/01/mesa-centro-fiji-700x700.webp"
  };
  
  // URLs genéricas para produtos sem imagem específica
  const imagemGenerica = "https://varandamix.com/wp-content/uploads/2023/12/sofa-interno.webp";
  
  // Aplicar imagens diretamente aos slides
  const slides = document.querySelectorAll('.product-swiper-wrapper .swiper-slide');
  console.log(`Encontrados ${slides.length} slides de produtos`);
  
  slides.forEach(function(slide) {
    const codeElement = slide.querySelector('.product-code');
    if (!codeElement) return;
    
    // Obter código do produto e limpar hífens
    const rawCode = codeElement.textContent.trim();
    const code = rawCode.replace(/-/g, '');
    
    console.log(`Processando produto: ${rawCode} (código limpo: ${code})`);
    
    // Buscar o wrapper de imagens
    const wrapper = slide.querySelector('.product-images .swiper-wrapper');
    if (!wrapper) return;
    
    // Usar imagem específica se disponível, ou genérica
    const imageUrl = imagensEstaticas[code] || imagensEstaticas[rawCode] || imagemGenerica;
    
    // Criar HTML para a imagem estática
    wrapper.innerHTML = `
      <div class="swiper-slide">
        <img src="${imageUrl}" loading="lazy" alt="Produto ${rawCode}" style="width: 100%; height: auto;">
      </div>
    `;
    
    console.log(`Imagem aplicada para ${code}: ${imageUrl}`);
  });
  
  console.log('Correção estática de imagens concluída');
});
