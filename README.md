# keinermendoza-load-markdown-to-db

Este projeto permite ler, carregar e atualizar dados em um banco de dados MySQL a partir de arquivos Markdown estruturados com frontmatter. É ideal para gerenciar o conteúdo do seu site de forma simples, utilizando apenas o seu editor de texto.

## Como funciona?

O programa mapeia automaticamente os arquivos contidos em três pastas (`tags`, `posts` e `projects`) para entidades do modelo de dados definido em `models.py` (`Tag`, `Post` e `Project`). Cada arquivo Markdown deve conter metadados (frontmatter) em formato YAML, que serão utilizados para preencher os campos do banco de dados.

A classe principal para leitura dos arquivos é `MarkdownDocument` (em `reader.py`). Essa classe expõe dois atributos principais:

- `metadata`: Um dicionário com os metadados extraídos do frontmatter.
- `content_html`: O conteúdo do arquivo convertido para HTML.

Para criar instâncias de `MarkdownDocument`, utiliza-se o método estático `from_file`, que recebe o caminho do arquivo e retorna uma instância pronta para uso.

## Requisitos

- Python 3.10+
- MySQL
- Dependências listadas em `requirements.txt`

## Instalação e uso

1. **Crie um ambiente virtual:**

```shell
   python -m venv venv
```

2. **Ative o ambiente virtual:**

```shell
source venv/bin/activate
```
3. **Instale as dependências:**

```shell
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Copie o arquivo .example.env e renomeie para .env

> Este programa assume que você tem acesso a um banco de dados MySQL. Utilize os valores de conexão do seu banco de dados, por exemplo:


```bash
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=localhost
DB_NAME=nome_do_seu_banco
```

5. **Execute o programa:**

```shell
python load.py
```

## Estrutura esperada dos arquivos Markdown

Cada arquivo deve conter um bloco de frontmatter YAML delimitado por --- no início e no final. Exemplo para uma tag:

```markdown
---
title: Laravel
description: Framework PHP elegante, expressivo e robusto, com um ecossistema rico de ferramentas para o desenvolvimento de aplicações web modernas.
image: /images/tags/laravel.png
is_public: true
---
```

## Inspiração

Este projeto é inspirado na facilidade de edição de conteúdo oferecida pelo framework Astro.js. O objetivo é permitir gerenciar o conteúdo do site diretamente a partir de arquivos Markdown.
