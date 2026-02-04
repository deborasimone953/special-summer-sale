// Script gerado automaticamente pela ferramenta aplicar_capas.py
// Este script atualiza as imagens de capa dos produtos selecionadas pela ferramenta selecionar_capa.py

window.addEventListener('DOMContentLoaded', function() {
  console.log("Aplicando imagens de capa atualizadas...");
  
  // Definição do objeto productImagesByCode com as capas atualizadas
  window.productImagesByCode = {
  "DV": [
    {
      desktop: "Sem categoria/DV-0045 - aparador Nature/Gemini_Generated_Image_ysf69zysf69zysf6-desktop.webp",
      mobile: "Sem categoria/DV-0045 - aparador Nature/Gemini_Generated_Image_ysf69zysf69zysf6-mobile.webp",
      full: "Sem categoria/DV-0045 - aparador Nature/Gemini_Generated_Image_ysf69zysf69zysf6.png"
    }
  ],
  "EX010": [
    {
      desktop: "Sem categoria/EX010 - SOF\u00c1 MANHATAN/Gemini_Generated_Image_cdn439cdn439cdn4-desktop.webp",
      mobile: "Sem categoria/EX010 - SOF\u00c1 MANHATAN/Gemini_Generated_Image_cdn439cdn439cdn4-mobile.webp",
      full: "Sem categoria/EX010 - SOF\u00c1 MANHATAN/Gemini_Generated_Image_cdn439cdn439cdn4.png"
    }
  ],
  "EX011": [
    {
      desktop: "Sem categoria/EX011 - OMBRELONE CENTRAL RIO DE JANEIRO/Foto 02-02-2026, 11 07 06-desktop.webp",
      mobile: "Sem categoria/EX011 - OMBRELONE CENTRAL RIO DE JANEIRO/Foto 02-02-2026, 11 07 06-mobile.webp",
      full: "Sem categoria/EX011 - OMBRELONE CENTRAL RIO DE JANEIRO/Foto 02-02-2026, 11 07 06.jpg"
    }
  ],
  "EX011B": [
    {
      desktop: "Sem categoria/EX011B - CADEIRA TRANCOSO C BRA\u00c7O/03be1f45-4d22-4f5c-b2aa-5b14836562c3-desktop.webp",
      mobile: "Sem categoria/EX011B - CADEIRA TRANCOSO C BRA\u00c7O/03be1f45-4d22-4f5c-b2aa-5b14836562c3-mobile.webp",
      full: "Sem categoria/EX011B - CADEIRA TRANCOSO C BRA\u00c7O/03be1f45-4d22-4f5c-b2aa-5b14836562c3.jpg"
    }
  ],
  "EX013": [
    {
      desktop: "Sem categoria/EX013 - CONJUNTO TRANCOSO/Gemini_Generated_Image_q5t5gvq5t5gvq5t5-desktop.webp",
      mobile: "Sem categoria/EX013 - CONJUNTO TRANCOSO/Gemini_Generated_Image_q5t5gvq5t5gvq5t5-mobile.webp",
      full: "Sem categoria/EX013 - CONJUNTO TRANCOSO/Gemini_Generated_Image_q5t5gvq5t5gvq5t5.png"
    }
  ],
  "EX014": [
    {
      desktop: "Sem categoria/EX014 - MESA ITAPARICA/Gemini_Generated_Image_vzx8j6vzx8j6vzx8-desktop.webp",
      mobile: "Sem categoria/EX014 - MESA ITAPARICA/Gemini_Generated_Image_vzx8j6vzx8j6vzx8-mobile.webp",
      full: "Sem categoria/EX014 - MESA ITAPARICA/Gemini_Generated_Image_vzx8j6vzx8j6vzx8.png"
    }
  ],
  "EX015": [
    {
      desktop: "Sem categoria/EX015 - CONJUNTO ITAPARICA/CONJUNTO ITAPARICA-01-desktop.webp",
      mobile: "Sem categoria/EX015 - CONJUNTO ITAPARICA/CONJUNTO ITAPARICA-01-mobile.webp",
      full: "Sem categoria/EX015 - CONJUNTO ITAPARICA/CONJUNTO ITAPARICA-01.png"
    }
  ],
  "EX016": [
    {
      desktop: "Sem categoria/EX016 - CADEIRA PARATI/Gemini_Generated_Image_vzx8j6vzx8j6vzx8-desktop.webp",
      mobile: "Sem categoria/EX016 - CADEIRA PARATI/Gemini_Generated_Image_vzx8j6vzx8j6vzx8-mobile.webp",
      full: "Sem categoria/EX016 - CADEIRA PARATI/Gemini_Generated_Image_vzx8j6vzx8j6vzx8.png"
    }
  ],
  "EX017": [
    {
      desktop: "Sem categoria/EX017 - MESA LATERAL MECA/Foto 31-07-2025, 17 22 10-desktop.webp",
      mobile: "Sem categoria/EX017 - MESA LATERAL MECA/Foto 31-07-2025, 17 22 10-mobile.webp",
      full: "Sem categoria/EX017 - MESA LATERAL MECA/Foto 31-07-2025, 17 22 10.jpg"
    }
  ],
  "EX018": [
    {
      desktop: "Sem categoria/EX018 - MESA GERIBA/c87e2532-7a5a-473d-ba33-312dc3ffaa2c-desktop.webp",
      mobile: "Sem categoria/EX018 - MESA GERIBA/c87e2532-7a5a-473d-ba33-312dc3ffaa2c-mobile.webp",
      full: "Sem categoria/EX018 - MESA GERIBA/c87e2532-7a5a-473d-ba33-312dc3ffaa2c.png"
    }
  ],
  "EX019": [
    {
      desktop: "Sem categoria/EX019 - CADEIRA GERIBA/Foto 02-02-2026, 11 07 06 (10)-desktop.webp",
      mobile: "Sem categoria/EX019 - CADEIRA GERIBA/Foto 02-02-2026, 11 07 06 (10)-mobile.webp",
      full: "Sem categoria/EX019 - CADEIRA GERIBA/Foto 02-02-2026, 11 07 06 (10).jpg"
    }
  ],
  "EX02": [
    {
      desktop: "Sem categoria/EX02 - POLTRONA BONINA/POLTRONA BONINA-01-desktop.webp",
      mobile: "Sem categoria/EX02 - POLTRONA BONINA/POLTRONA BONINA-01-mobile.webp",
      full: "Sem categoria/EX02 - POLTRONA BONINA/POLTRONA BONINA-01.png"
    }
  ],
  "EX020": [
    {
      desktop: "Sem categoria/EX020 - CONJUNTO TAU\u00cdPE/CONJUNTO TAU\u00cdPE-02-desktop.webp",
      mobile: "Sem categoria/EX020 - CONJUNTO TAU\u00cdPE/CONJUNTO TAU\u00cdPE-02-mobile.webp",
      full: "Sem categoria/EX020 - CONJUNTO TAU\u00cdPE/CONJUNTO TAU\u00cdPE-02.png"
    }
  ],
  "EX03": [
    {
      desktop: "Sem categoria/EX03 - MESA LATERAL RUEDA/MESA LATERAL RUEDA-01-desktop.webp",
      mobile: "Sem categoria/EX03 - MESA LATERAL RUEDA/MESA LATERAL RUEDA-01-mobile.webp",
      full: "Sem categoria/EX03 - MESA LATERAL RUEDA/MESA LATERAL RUEDA-01.png"
    }
  ],
  "EX04": [
    {
      desktop: "Sem categoria/EX04 - TAPETE ARA/Foto 06-12-2023, 16 59 12-desktop.webp",
      mobile: "Sem categoria/EX04 - TAPETE ARA/Foto 06-12-2023, 16 59 12-mobile.webp",
      full: "Sem categoria/EX04 - TAPETE ARA/Foto 06-12-2023, 16 59 12.jpg"
    }
  ],
  "EX07": [
    {
      desktop: "Sem categoria/EX07 - BALAN\u00c7O LUAR/BALAN\u00c7O LUAR-02-desktop.webp",
      mobile: "Sem categoria/EX07 - BALAN\u00c7O LUAR/BALAN\u00c7O LUAR-02-mobile.webp",
      full: "Sem categoria/EX07 - BALAN\u00c7O LUAR/BALAN\u00c7O LUAR-02.jpg"
    }
  ],
  "EX08": [
    {
      desktop: "Sem categoria/EX08 - BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O/BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O-02-desktop.webp",
      mobile: "Sem categoria/EX08 - BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O/BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O-02-mobile.webp",
      full: "Sem categoria/EX08 - BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O/BALAN\u00c7O LUAR COM SUPORTE DE CH\u00c3O-02.jpg"
    }
  ],
  "EX09": [
    {
      desktop: "Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4-desktop.webp",
      mobile: "Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4-mobile.webp",
      full: "Sem categoria/EX09 - ESPREGUICADEIRA BUZIOS/26818fb6-65e6-43bb-9f7a-1149feec78f4.jpg"
    }
  ],
  "ML": [
    {
      desktop: "Sem categoria/ML-0031 - Mesa Lateral Atria/19e5b1c2-41ec-4d63-8c2f-695047a8686c-desktop.webp",
      mobile: "Sem categoria/ML-0031 - Mesa Lateral Atria/19e5b1c2-41ec-4d63-8c2f-695047a8686c-mobile.webp",
      full: "Sem categoria/ML-0031 - Mesa Lateral Atria/19e5b1c2-41ec-4d63-8c2f-695047a8686c.jpg"
    }
  ],
  "PROD-1225": [
    {
      desktop: "Sem categoria/PROD-1225 - Poltrona round/Poltrona round-01-desktop.webp",
      mobile: "Sem categoria/PROD-1225 - Poltrona round/Poltrona round-01-mobile.webp",
      full: "Sem categoria/PROD-1225 - Poltrona round/Poltrona round-01.jpg"
    }
  ],
  "PROD-1433": [
    {
      desktop: "Sem categoria/PROD-1433 - Mesa creta/Foto 14-11-2025, 18 12 01-desktop.webp",
      mobile: "Sem categoria/PROD-1433 - Mesa creta/Foto 14-11-2025, 18 12 01-mobile.webp",
      full: "Sem categoria/PROD-1433 - Mesa creta/Foto 14-11-2025, 18 12 01.jpg"
    }
  ],
  "PROD-1931": [
    {
      desktop: "Sem categoria/PROD-1931 - Poltrona Nuvem/Poltrona Nuvem-03-desktop.webp",
      mobile: "Sem categoria/PROD-1931 - Poltrona Nuvem/Poltrona Nuvem-03-mobile.webp",
      full: "Sem categoria/PROD-1931 - Poltrona Nuvem/Poltrona Nuvem-03.png"
    }
  ],
  "PROD-2471": [
    {
      desktop: "Sem categoria/PROD-2471 - Sof\u00e1 Brisa/Foto 27-03-2025, 12 11 16-desktop.webp",
      mobile: "Sem categoria/PROD-2471 - Sof\u00e1 Brisa/Foto 27-03-2025, 12 11 16-mobile.webp",
      full: "Sem categoria/PROD-2471 - Sof\u00e1 Brisa/Foto 27-03-2025, 12 11 16.jpg"
    }
  ],
  "PROD-2665": [
    {
      desktop: "Sem categoria/PROD-2665 - Poltrona Sola/Foto 07-02-2024, 14 32 38-desktop.webp",
      mobile: "Sem categoria/PROD-2665 - Poltrona Sola/Foto 07-02-2024, 14 32 38-mobile.webp",
      full: "Sem categoria/PROD-2665 - Poltrona Sola/Foto 07-02-2024, 14 32 38.jpg"
    }
  ],
  "PROD-2698": [
    {
      desktop: "Sem categoria/PROD-2698 - Cadeira Siena/Gemini_Generated_Image_83lcta83lcta83lc-desktop.webp",
      mobile: "Sem categoria/PROD-2698 - Cadeira Siena/Gemini_Generated_Image_83lcta83lcta83lc-mobile.webp",
      full: "Sem categoria/PROD-2698 - Cadeira Siena/Gemini_Generated_Image_83lcta83lcta83lc.png"
    }
  ],
  "PROD-2787": [
    {
      desktop: "Sem categoria/PROD-2787 - Poltrona hope/Foto 07-10-2024, 09 46 18-desktop.webp",
      mobile: "Sem categoria/PROD-2787 - Poltrona hope/Foto 07-10-2024, 09 46 18-mobile.webp",
      full: "Sem categoria/PROD-2787 - Poltrona hope/Foto 07-10-2024, 09 46 18.jpg"
    }
  ],
  "PROD-3028": [
    {
      desktop: "Sem categoria/PROD-3028 - Cadeira Neve/Gemini_Generated_Image_ot2wi2ot2wi2ot2w-desktop.webp",
      mobile: "Sem categoria/PROD-3028 - Cadeira Neve/Gemini_Generated_Image_ot2wi2ot2wi2ot2w-mobile.webp",
      full: "Sem categoria/PROD-3028 - Cadeira Neve/Gemini_Generated_Image_ot2wi2ot2wi2ot2w.png"
    }
  ],
  "PROD-3613": [
    {
      desktop: "Sem categoria/PROD-3613 - Poltrona Carbono/Gemini_Generated_Image_qypo1zqypo1zqypo-desktop.webp",
      mobile: "Sem categoria/PROD-3613 - Poltrona Carbono/Gemini_Generated_Image_qypo1zqypo1zqypo-mobile.webp",
      full: "Sem categoria/PROD-3613 - Poltrona Carbono/Gemini_Generated_Image_qypo1zqypo1zqypo.png"
    }
  ],
  "PROD-3893": [
    {
      desktop: "Sem categoria/PROD-3893 - Poltrona nux/Poltrona nux-02-desktop.webp",
      mobile: "Sem categoria/PROD-3893 - Poltrona nux/Poltrona nux-02-mobile.webp",
      full: "Sem categoria/PROD-3893 - Poltrona nux/Poltrona nux-02.png"
    }
  ],
  "PROD-3925": [
    {
      desktop: "Sem categoria/PROD-3925 - Cadeira Melia/Cadeira Melia-02-desktop.webp",
      mobile: "Sem categoria/PROD-3925 - Cadeira Melia/Cadeira Melia-02-mobile.webp",
      full: "Sem categoria/PROD-3925 - Cadeira Melia/Cadeira Melia-02.jpg"
    }
  ],
  "PROD-4091": [
    {
      desktop: "Sem categoria/PROD-4091 - Poltrona pitia/Poltrona pitia-01-desktop.webp",
      mobile: "Sem categoria/PROD-4091 - Poltrona pitia/Poltrona pitia-01-mobile.webp",
      full: "Sem categoria/PROD-4091 - Poltrona pitia/Poltrona pitia-01.jpg"
    }
  ],
  "PROD-4263": [
    {
      desktop: "Sem categoria/PROD-4263 - Poltrona sett/Poltrona sett-04-desktop.webp",
      mobile: "Sem categoria/PROD-4263 - Poltrona sett/Poltrona sett-04-mobile.webp",
      full: "Sem categoria/PROD-4263 - Poltrona sett/Poltrona sett-04.png"
    }
  ],
  "PROD-4523": [
    {
      desktop: "Sem categoria/PROD-4523 - Mesa feixe/Mesa feixe-01-desktop.webp",
      mobile: "Sem categoria/PROD-4523 - Mesa feixe/Mesa feixe-01-mobile.webp",
      full: "Sem categoria/PROD-4523 - Mesa feixe/Mesa feixe-01.jpg"
    }
  ],
  "PROD-4740": [
    {
      desktop: "Sem categoria/PROD-4740 - Poltrona Tela/Poltrona Tela-02-desktop.webp",
      mobile: "Sem categoria/PROD-4740 - Poltrona Tela/Poltrona Tela-02-mobile.webp",
      full: "Sem categoria/PROD-4740 - Poltrona Tela/Poltrona Tela-02.jpg"
    }
  ],
  "PROD-5921": [
    {
      desktop: "Sem categoria/PROD-5921 - Cadeira Giro/Cadeira Giro-04-desktop.webp",
      mobile: "Sem categoria/PROD-5921 - Cadeira Giro/Cadeira Giro-04-mobile.webp",
      full: "Sem categoria/PROD-5921 - Cadeira Giro/Cadeira Giro-04.jpg"
    }
  ],
  "PROD-6305": [
    {
      desktop: "Sem categoria/PROD-6305 - Poltrona Luar/Gemini_Generated_Image_jg08fojg08fojg08-desktop.webp",
      mobile: "Sem categoria/PROD-6305 - Poltrona Luar/Gemini_Generated_Image_jg08fojg08fojg08-mobile.webp",
      full: "Sem categoria/PROD-6305 - Poltrona Luar/Gemini_Generated_Image_jg08fojg08fojg08.png"
    }
  ],
  "PROD-6411": [
    {
      desktop: "Sem categoria/PROD-6411 - Cadeira Horizonte/3e7f8715-7b1d-492f-81a5-eaa9936a0742-desktop.webp",
      mobile: "Sem categoria/PROD-6411 - Cadeira Horizonte/3e7f8715-7b1d-492f-81a5-eaa9936a0742-mobile.webp",
      full: "Sem categoria/PROD-6411 - Cadeira Horizonte/3e7f8715-7b1d-492f-81a5-eaa9936a0742.png"
    }
  ],
  "PROD-6666": [
    {
      desktop: "Sem categoria/PROD-6666 - Mesa Cristal/a718d011-81dd-4bb6-85da-730af489d2d3-desktop.webp",
      mobile: "Sem categoria/PROD-6666 - Mesa Cristal/a718d011-81dd-4bb6-85da-730af489d2d3-mobile.webp",
      full: "Sem categoria/PROD-6666 - Mesa Cristal/a718d011-81dd-4bb6-85da-730af489d2d3.png"
    }
  ],
  "PROD-6749": [
    {
      desktop: "Sem categoria/PROD-6749 - Mesa de centro Bruma/Mesa de centro Bruma-02-desktop.webp",
      mobile: "Sem categoria/PROD-6749 - Mesa de centro Bruma/Mesa de centro Bruma-02-mobile.webp",
      full: "Sem categoria/PROD-6749 - Mesa de centro Bruma/Mesa de centro Bruma-02.png"
    }
  ],
  "PROD-6900": [
    {
      desktop: "Sem categoria/PROD-6900 - Mesa de centro Duetto/Gemini_Generated_Image_tntqpztntqpztntqpppp-desktop.webp",
      mobile: "Sem categoria/PROD-6900 - Mesa de centro Duetto/Gemini_Generated_Image_tntqpztntqpztntqpppp-mobile.webp",
      full: "Sem categoria/PROD-6900 - Mesa de centro Duetto/Gemini_Generated_Image_tntqpztntqpztntqpppp.png"
    }
  ],
  "PROD-7091": [
    {
      desktop: "Sem categoria/PROD-7091 - Cadeira Jangada/2e2f5467-bff2-4b0e-b416-115aa1ce78ba-desktop.webp",
      mobile: "Sem categoria/PROD-7091 - Cadeira Jangada/2e2f5467-bff2-4b0e-b416-115aa1ce78ba-mobile.webp",
      full: "Sem categoria/PROD-7091 - Cadeira Jangada/2e2f5467-bff2-4b0e-b416-115aa1ce78ba.png"
    }
  ],
  "PROD-7289": [
    {
      desktop: "Sem categoria/PROD-7289 - Mesa de centro orga/Mesa de centro orga-01-desktop.webp",
      mobile: "Sem categoria/PROD-7289 - Mesa de centro orga/Mesa de centro orga-01-mobile.webp",
      full: "Sem categoria/PROD-7289 - Mesa de centro orga/Mesa de centro orga-01.jpg"
    }
  ],
  "PROD-7420": [
    {
      desktop: "Sem categoria/PROD-7420 - Poltrona Eclipse/8b3cb09a-6327-4220-bb29-f62e55538445-desktop.webp",
      mobile: "Sem categoria/PROD-7420 - Poltrona Eclipse/8b3cb09a-6327-4220-bb29-f62e55538445-mobile.webp",
      full: "Sem categoria/PROD-7420 - Poltrona Eclipse/8b3cb09a-6327-4220-bb29-f62e55538445.png"
    }
  ],
  "PROD-8075": [
    {
      desktop: "Sem categoria/PROD-8075 - Poltrona malva/Poltrona malva-04-desktop.webp",
      mobile: "Sem categoria/PROD-8075 - Poltrona malva/Poltrona malva-04-mobile.webp",
      full: "Sem categoria/PROD-8075 - Poltrona malva/Poltrona malva-04.jpg"
    }
  ],
  "PROD-8087": [
    {
      desktop: "Sem categoria/PROD-8087 - cadeira aurora/Foto 30-01-2026, 17 01 28 (3)-desktop.webp",
      mobile: "Sem categoria/PROD-8087 - cadeira aurora/Foto 30-01-2026, 17 01 28 (3)-mobile.webp",
      full: "Sem categoria/PROD-8087 - cadeira aurora/Foto 30-01-2026, 17 01 28 (3).jpg"
    }
  ],
  "PROD-8953": [
    {
      desktop: "Sem categoria/PROD-8953 - Mesa de centro eixo/Gemini_Generated_Image_aqiu3gaqiu3gaqiu-desktop.webp",
      mobile: "Sem categoria/PROD-8953 - Mesa de centro eixo/Gemini_Generated_Image_aqiu3gaqiu3gaqiu-mobile.webp",
      full: "Sem categoria/PROD-8953 - Mesa de centro eixo/Gemini_Generated_Image_aqiu3gaqiu3gaqiu.png"
    }
  ],
  "PROD-9459": [
    {
      desktop: "Sem categoria/PROD-9459 - Poltrona Algod\u00e3o/be36b989-7e69-4bed-bf89-d293a99c0a7e-desktop.webp",
      mobile: "Sem categoria/PROD-9459 - Poltrona Algod\u00e3o/be36b989-7e69-4bed-bf89-d293a99c0a7e-mobile.webp",
      full: "Sem categoria/PROD-9459 - Poltrona Algod\u00e3o/be36b989-7e69-4bed-bf89-d293a99c0a7e.png"
    }
  ],
  "PROD-9976": [
    {
      desktop: "Sem categoria/PROD-9976 - Mesa hunt/Mesa hunt-03-desktop.webp",
      mobile: "Sem categoria/PROD-9976 - Mesa hunt/Mesa hunt-03-mobile.webp",
      full: "Sem categoria/PROD-9976 - Mesa hunt/Mesa hunt-03.jpg"
    }
  ],
  "VMSF01": [
    {
      desktop: "Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27-desktop.webp",
      mobile: "Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27-mobile.webp",
      full: "Sem categoria/VMSF01 - SOFA ORGANICO NAPOLI/Foto 19-10-2023, 08 42 27.jpg"
    }
  ],
  "VMSF02": [
    {
      desktop: "Sem categoria/VMSF02 - SOF\u00c1 MERIDIAN/Foto 27-03-2025, 12 12 07-desktop.webp",
      mobile: "Sem categoria/VMSF02 - SOF\u00c1 MERIDIAN/Foto 27-03-2025, 12 12 07-mobile.webp",
      full: "Sem categoria/VMSF02 - SOF\u00c1 MERIDIAN/Foto 27-03-2025, 12 12 07.jpg"
    }
  ],
  "VMSF03": [
    {
      desktop: "Sem categoria/VMSF03 - SOF\u00c1 OAK/SOF\u00c1 OAK-01-desktop.webp",
      mobile: "Sem categoria/VMSF03 - SOF\u00c1 OAK/SOF\u00c1 OAK-01-mobile.webp",
      full: "Sem categoria/VMSF03 - SOF\u00c1 OAK/SOF\u00c1 OAK-01.png"
    }
  ],
  "VMSF04": [
    {
      desktop: "Sem categoria/VMSF04 - SOF\u00c1 LATT/SOF\u00c1 LATT-02-desktop.webp",
      mobile: "Sem categoria/VMSF04 - SOF\u00c1 LATT/SOF\u00c1 LATT-02-mobile.webp",
      full: "Sem categoria/VMSF04 - SOF\u00c1 LATT/SOF\u00c1 LATT-02.jpg"
    }
  ]
};
  
  // Aplicar as imagens após um pequeno atraso
  setTimeout(function() {
    if (typeof window.applyProductImages === 'function') {
      console.log('Aplicando imagens aos produtos...');
      window.applyProductImages();
      
      // Verificação para garantir que as imagens foram aplicadas
      setTimeout(function() {
        console.log('Verificando aplicação de imagens...');
        window.applyProductImages();
        console.log('Produtos disponíveis:', Object.keys(window.productImagesByCode).length);
      }, 500);
    } else {
      console.error('Função applyProductImages não encontrada!');
    }
  }, 200);
});
