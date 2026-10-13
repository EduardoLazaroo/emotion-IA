# Apresentação Profissional: Emotionfy (Emotion-IA)

## 1. Identidade e Proposta de Valor

O **Emotionfy** é uma aplicação de sinestesia computacional que une música, processamento de linguagem natural e inteligência artificial generativa em uma experiência imersiva contínua. O projeto explora a ponte entre o consumo passivo de áudio no **Spotify** e a expressão visual personalizada, transformando o conteúdo semântico e afetivo de letras musicais em paletas cromáticas e artes visuais sintetizadas por **DALL-E 3**.

Em termos de engenharia, a solução se destaca por uma **arquitetura distribuída de microserviços desacoplados**: um API Gateway em Flask gerencia o ciclo de autorização OAuth 2.0 e raspagem resiliente de letras no **Genius**, enquanto um serviço autônomo de inteligência artificial decompõe letras em 8 dimensões semântico-afetivas e orquestra a geração de imagens de alta resolução.

---

## 2. Destaques Técnicos e Decisões de Arquitetura

1. **Separação de Preocupações (Gateway vs IA)**: O isolamento da lógica de IA na porta 5001 (`analise.py`) protege o Gateway na porta 5000 (`main.py`), permitindo escalabilidade horizontal independente de requisições de geração de imagem.
2. **Decomposição Afetiva Estruturada em 8 Dimensões**: Em vez de passar prompts genéricos para modelos de imagem, o sistema realiza uma análise multidimensional rigorosa (emoção, tríade cromática, tema, tom narrativo, mensagem central, figuras de linguagem e palavras-chave), garantindo que a arte gerada reflita a identidade lírica do artista.
3. **Resiliência e Segurança em OAuth**: Fluxo completo de autorização OAuth com escopos restritos de leitura de streaming (`user-read-currently-playing`), validação de códigos temporários e proteção de rotas com HTTP 401 para requisições não autenticadas.
4. **Scraping Estruturado e Robusto**: Extração de letras via `BeautifulSoup` adaptada às estruturas modernas do Genius (`data-lyrics-container`), contornando limitações de metadados truncados.

---

## 3. Texto Executivo para Divulgação / Portfólio

> "A sinestesia computacional abre fronteiras inéditas para a conexão emocional entre ouvintes e música. No projeto **Emotionfy**, projetei e implementei uma arquitetura distribuída em **Flask** conectando a API do **Spotify**, o catálogo do **Genius** e os modelos de ponta da **OpenAI (GPT e DALL-E 3)**.
>
> A solução opera com um API Gateway encarregado de OAuth 2.0 e identificação da faixa em streaming em tempo real, associado a um microserviço de IA que decompõe a letra em 8 atributos afetivos e cromáticos. A partir dessa sinestesia estruturada, o sistema gera dinamicamente telas conceituais únicas que expressam a alma da canção.
>
> Os testes integrados atestaram conformidade estrita de rotas, robustez nos seletores de scraping e síntese artística de alta fidelidade visual, ilustrando o poder da inteligência artificial generativa aplicada à experiência musical moderna."

---

## 4. Evidências Empíricas e Visuais Disponíveis

- [`evidencias/arquitetura_emotionfy.png`](evidencias/arquitetura_emotionfy.png): Diagrama da arquitetura distribuída conectando Frontend, API Gateway (5000), Microserviço IA (5001) e as APIs externas.
- [`evidencias/fluxo_sinestesia_emocional_ia.png`](evidencias/fluxo_sinestesia_emocional_ia.png): Infográfico das 8 dimensões psicológicas e cromáticas extraídas da lírica musical e montagem do prompt gerativo.
- [`evidencias/log_execucao_real.txt`](evidencias/log_execucao_real.txt): Registro fidedigno das requisições reais executadas no microserviço e no gateway, comprovando tratamento de erros e respostas estruturadas.
