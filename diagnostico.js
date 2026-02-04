// Script de diagnóstico para verificar problemas com as imagens
console.log("=== DIAGNÓSTICO DE IMAGENS ===");

// Verificar se o objeto productImagesByCode existe
console.log("productImagesByCode existe:", typeof window.productImagesByCode !== 'undefined');
if (typeof window.productImagesByCode !== 'undefined') {
  console.log("Número de produtos mapeados:", Object.keys(window.productImagesByCode).length);
  
  // Listar alguns códigos de produtos no mapeamento
  console.log("Amostra de códigos de produtos:", Object.keys(window.productImagesByCode).slice(0, 10));
  
  // Verificar alguns produtos específicos
  const produtosParaChecar = ["EX01", "EX-01", "VMSF01", "VMSF-01", "A-0001"];
  produtosParaChecar.forEach(codigo => {
    console.log(`Produto ${codigo} existe:`, !!window.productImagesByCode[codigo]);
  });
}

// Verificar se a função applyProductImages existe
console.log("applyProductImages existe:", typeof window.applyProductImages === 'function');

// Verificar elementos da página
console.log("Slides de produtos encontrados:", document.querySelectorAll('.product-swiper-wrapper .swiper-slide').length);

// Tentar aplicar as imagens manualmente
console.log("Tentando aplicar imagens manualmente...");

document.querySelectorAll('.product-swiper-wrapper .swiper-slide').forEach((slide) => {
  const codeElement = slide.querySelector('.product-code');
  if (!codeElement) {
    console.log("Slide sem código de produto");
    return;
  }
  
  const code = codeElement.textContent.trim();
  console.log(`Verificando produto: ${code}`);
  
  let images = null;
  
  // Tentar várias formas do código
  if (window.productImagesByCode) {
    images = window.productImagesByCode[code] || 
             window.productImagesByCode[code.replace('-', '')] ||
             window.productImagesByCode[code.replace('', '-')] || 
             window.productImagesByCode[String(code).toUpperCase()];
  }
  
  if (!images || !images.length) {
    console.log(`Imagens não encontradas para: ${code}`);
    return;
  }
  
  console.log(`Imagens encontradas para ${code}: ${images.length}`);
  
  const wrapper = slide.querySelector('.product-images .swiper-wrapper');
  if (!wrapper) {
    console.log(`Wrapper de imagens não encontrado para ${code}`);
    return;
  }
  
  try {
    if (typeof window.buildImageSlide === 'function') {
      wrapper.innerHTML = images.map(window.buildImageSlide).join('');
      console.log(`Imagens aplicadas para ${code}`);
    } else {
      console.log("Função buildImageSlide não encontrada");
    }
  } catch (e) {
    console.error(`Erro ao aplicar imagens para ${code}:`, e);
  }
});

console.log("=== FIM DO DIAGNÓSTICO ===");
