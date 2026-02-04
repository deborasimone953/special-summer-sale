// Script otimizado para evitar problemas de Content Security Policy
document.addEventListener('DOMContentLoaded', function() {
  console.log("Iniciando correção com compatibilidade CSP...");
  
  // Função para criar HTML do slide de imagem sem usar eval
  function createImageSlide(image) {
    return '<div class="swiper-slide"><img src="' + image.desktop + 
           '" srcset="' + image.desktop + ' 1x, ' + image.full + ' 2x" loading="lazy" alt=""></div>';
  }
  
  // Mapear imagens para produtos específicos (códigos sem hífen)
  const imageMapping = {
    // Produto específicos com suas imagens correspondentes
    "EX019": [
      {
        desktop: "assets/fotos/Sem categoria/EX019 - CADEIRA GERIBA/e3ee487d-bff1-4953-834b-a230ebe5ccc9-desktop.webp",
        mobile: "assets/fotos/Sem categoria/EX019 - CADEIRA GERIBA/e3ee487d-bff1-4953-834b-a230ebe5ccc9-mobile.webp",
        full: "assets/fotos/Sem categoria/EX019 - CADEIRA GERIBA/e3ee487d-bff1-4953-834b-a230ebe5ccc9.jpg"
      }
    ],
    "EX021": [
      {
        desktop: "assets/fotos/Sem categoria/EX021 - CADEIRA ITA/Foto 31-07-2025, 17 22 47-desktop.webp",
        mobile: "assets/fotos/Sem categoria/EX021 - CADEIRA ITA/Foto 31-07-2025, 17 22 47-mobile.webp",
        full: "assets/fotos/Sem categoria/EX021 - CADEIRA ITA/Foto 31-07-2025, 17 22 47.jpg"
      }
    ],
    "EX016": [
      {
        desktop: "assets/fotos/Sem categoria/EX016 - CADEIRA PARATI/51622331-3f1b-424c-b29a-7d9a7f923750-desktop.webp",
        mobile: "assets/fotos/Sem categoria/EX016 - CADEIRA PARATI/51622331-3f1b-424c-b29a-7d9a7f923750-mobile.webp",
        full: "assets/fotos/Sem categoria/EX016 - CADEIRA PARATI/51622331-3f1b-424c-b29a-7d9a7f923750.jpg"
      }
    ],
    "EX011B": [
      {
        desktop: "assets/fotos/Sem categoria/EX011B - CADEIRA TRANCOSO C BRAÇO/03be1f45-4d22-4f5c-b2aa-5b14836562c3-desktop.webp",
        mobile: "assets/fotos/Sem categoria/EX011B - CADEIRA TRANCOSO C BRAÇO/03be1f45-4d22-4f5c-b2aa-5b14836562c3-mobile.webp",
        full: "assets/fotos/Sem categoria/EX011B - CADEIRA TRANCOSO C BRAÇO/03be1f45-4d22-4f5c-b2aa-5b14836562c3.jpg"
      }
    ],
    "EX09": [
      {
        desktop: "assets/fotos/Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4-desktop.webp",
        mobile: "assets/fotos/Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4-mobile.webp",
        full: "assets/fotos/Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4.jpg"
      }
    ],
    "VMSF01": [
      {
        desktop: "assets/fotos/Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27-desktop.webp",
        mobile: "assets/fotos/Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27-mobile.webp",
        full: "assets/fotos/Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27.jpg"
      }
    ]
  };
  
  // Aplicar imagens diretamente
  const slides = document.querySelectorAll('.product-swiper-wrapper .swiper-slide');
  console.log(`Encontrados ${slides.length} slides de produtos`);
  
  if (slides.length === 0) {
    console.log("Nenhum slide de produto encontrado na página");
  }
  
  slides.forEach(function(slide) {
    const codeElement = slide.querySelector('.product-code');
    if (!codeElement) {
      console.log("Slide sem código de produto");
      return;
    }
    
    // Obter código do produto e limpar hífens
    const rawCode = codeElement.textContent.trim();
    const code = rawCode.replace(/-/g, '');
    
    console.log(`Processando produto: ${rawCode} (código limpo: ${code})`);
    
    // Tentar encontrar imagens para este código
    const images = imageMapping[code] || imageMapping[rawCode];
    
    if (!images || images.length === 0) {
      console.log(`Nenhuma imagem encontrada para: ${code}`);
      return;
    }
    
    console.log(`Encontradas ${images.length} imagens para ${code}`);
    
    // Encontrar o wrapper de imagens
    const wrapper = slide.querySelector('.product-images .swiper-wrapper');
    if (!wrapper) {
      console.log(`Wrapper de imagens não encontrado para: ${code}`);
      return;
    }
    
    // Aplicar imagens usando nossa função segura
    const imageHTML = images.map(createImageSlide).join('');
    wrapper.innerHTML = imageHTML;
    console.log(`Imagens aplicadas para: ${code}`);
  });
  
  console.log("Aplicação de imagens concluída");
});
