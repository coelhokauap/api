# Coca combina?

Aplicação de terminal que permite pesquisar uma comida, escolher um prato retornado pela API e receber uma recomendação simples sobre se ele combina com Coca-Cola.

## API utilizada

O projeto consulta a [TheMealDB](https://www.themealdb.com/), uma API pública de receitas. A busca por nome usa uma requisição HTTP GET ao endpoint `search.php`, com o termo enviado no parâmetro `s`. A resposta JSON contém a lista `meals`; cada prato pode incluir nome (`strMeal`), categoria (`strCategory`), região (`strArea`) e ingredientes (`strIngredient1` a `strIngredient20`). Quando não há resultados, `meals` é `null`.

Documentação: [TheMealDB API Guide](https://www.themealdb.com/docs_api_guide.php).

## Como executar

Requer Python 3.9 ou mais recente.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Digite uma busca, escolha um dos pratos encontrados e veja a recomendação. A busca funciona melhor com nomes em inglês, como `chicken` ou `cake`. Após escolher um prato, o app mostra uma lista simples com o nome e o link do vídeo, e salva essa seleção em `dados_api.json`.

## Como funciona a recomendação

A função `recomendar_com_coca` usa a categoria do prato retornada pela API para dar uma sugestão simples. Não é uma avaliação científica de sabor; a preferência pessoal pode ser diferente.

## Tratamento de erros

O programa trata falhas de conexão, timeout, status HTTP inválido e JSON malformado. Também permite sair da seleção e informa quando a busca não encontra pratos.

## Arquivos

- `main.py`: busca, seleção, recomendação e tratamento de erros.
- `requirements.txt`: dependência HTTP do projeto.
- `dados_api.json`: lista simples com o prato escolhido e o link do vídeo da receita; atualizada a cada seleção.
