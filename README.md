# Emotionfy

## Visao geral

Emotionfy e uma aplicacao web experimental que conecta a faixa atual de um usuario do Spotify a uma experiencia de analise emocional e geracao visual. O fluxo autentica o usuario, consulta a faixa em reproducao, procura a letra por meio do Genius e encaminha a analise e a geracao de imagem aos servicos configurados.

O projeto e destinado a demonstracoes de integracao entre musica, interfaces web e IA. Nao deve ser apresentado como uma analise psicologica, clinica ou objetiva das letras.

## Arquitetura

| Camada | Tecnologia e responsabilidade |
|---|---|
| Aplicacao web | Flask |
| Interface | HTML, CSS e JavaScript |
| Musica | Spotify OAuth e Spotify Web API |
| Letras | Genius |
| Analise e imagem | integracoes de IA configuradas pelo ambiente |

As rotas estao em `app/routes.py`; as integracoes do Spotify e do Genius estao em `app/spotify.py` e `app/genius.py`; os templates ficam em `app/templates/`.

## Requisitos

- Python 3.10 ou superior;
- conta e aplicacao configurada no Spotify Developer Dashboard;
- credenciais do Genius;
- credenciais dos servicos de IA usados pelo ambiente;
- servico complementar de analise/geracao disponivel em `127.0.0.1:5001`, quando exigido pelas rotas.

## Instalacao

Na raiz do projeto:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crie um arquivo `.env` com as credenciais que a aplicacao requer. Os nomes exatos das variaveis devem ser confirmados no codigo e no arquivo de exemplo, quando disponivel. Nunca versione credenciais reais.

## Execucao

O ponto de entrada presente no repositorio e `main.py`:

```bash
python main.py
```

Com o servidor iniciado, acesse `http://localhost:5000`.

Antes de testar o fluxo completo, confirme que a URL de retorno cadastrada no Spotify corresponde ao ambiente local e que o servico complementar na porta 5001 esta acessivel. Sem essas configuracoes, o login, a analise ou a imagem podem falhar.

## Funcionalidades verificadas

- autenticacao por Spotify OAuth;
- consulta da faixa atual;
- busca de letra via Genius;
- interface para apresentar a leitura emocional;
- interface para apresentar e baixar uma imagem gerada.

## Limites conhecidos

- a aplicacao depende de credenciais e servicos externos;
- o servico local na porta 5001 nao esta documentado como parte deste repositorio;
- nao foi identificada suite automatizada de testes;
- custos, limites de requisicao e tratamento de indisponibilidade dos provedores devem ser considerados antes de qualquer implantacao.

## Apresentacao profissional

O texto de publicacao, as capturas recomendadas e o prompt de imagem estao em [APRESENTACAO.md](APRESENTACAO.md).
