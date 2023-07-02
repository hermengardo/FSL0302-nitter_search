# FSL0302-nitter_search
[![CodeFactor](https://www.codefactor.io/repository/github/hermengardo/fsl0302-nitter_search/badge)](https://www.codefactor.io/repository/github/hermengardo/fsl0302-nitter_search)

## **Introdução**
- Web scraper desenvolvido para coletar tweets do Nitter.net, um front-end alternativo ao Twitter que se concentra em oferecer maior privacidade aos usuários.
- Este scraper é especialmente útil para pesquisadores e analistas de dados que desejam coletar tweets sem depender de uma conta ou da API do Twitter.
- Desenvolvido para a matéria de Práticas de Pesquisa em Sociologia (USP/2023).

## **Instalação**
1. Clone o repositório:
```sh
git clone https://github.com/hermengardo/FSL0302-nitter_search.git
```

2. Instale as dependências:
```sh
pip install -r requirements.txt
```

3. Edite e execute o arquivo `main.py`.

### Exemplo de uso

```python
from scraper import NitterSearch

def main():
    NitterSearch(query='sua_query')


if __name__ == "__main__":
    main()
```

## **Parâmetros**

| Parâmetro | Tipo | Descrição | Opcional |
| --- | --- | --- | --- |
| `query` | str | Consulta usada para buscar os tweets. | Não |
| `file_path` | str | Arquivo onde os dados serão salvos. O padrão é 'data.csv'. | Sim |
| `delay` | float | Tempo de espera entre uma solitação (request) e outra. O padrão é 0,01 segundos. | Sim |
| `random_time` | bool | Indica se um tempo aleatório deve ser adicionado ao delay. O padrão é `False`. | Sim |
| `random_interval` | tuple | Intervalo de tempo aleatório. O padrão é (0, 1), i.e. um tempo aleatório entre 0 e 1 segundo será adicionado a cada solicitação de coleta (caso `random_time=True`). | Sim |
| `seed` | int | Seed do gerador de números pseudoaleatórios. | Sim |
| `timeout_wait` | int | Tempo de espera (em segundos) antes de tentar novamente se ocorrer um erro de tempo limite de conexão ou de leitura. O padrão é 60 segundos. | Sim |
| `retries` | int | Número máximo de vezes que a classe tentará fazer a solicitação novamente se ocorrer um erro de tempo limite de conexão ou de leitura. O padrão é 3. | Sim |

## **Campos disponíveis**

| Variável      | Descrição                                                   | Tipo |
|---------------|-------------------------------------------------------------|--------------|
| fullname      | Nome completo do autor da publicação                         | str          |
| username      | Nome de usuário do autor da publicação                       | str          |
| content       | Texto da publicação                                          | str          |
| publishedAt   | Data e hora em que a publicação foi feita                     | str          |
| comments      | Número de comentários na publicação                          | int          |
| retweets      | Número de retweets da publicação                              | int          |
| quotes        | Número de citações da publicação                              | int          |
| hearts        | Número de curtidas/likes da publicação                        | int          |
| imgAvatar     | URL da foto de perfil do autor da publicação                  | str          |
| images        | URLs das imagens incluídas na publicação                      | List[str]    |
| videos        | URLs dos vídeos incluídos na publicação                       | List[str]    |
| mentions      | Nomes de usuários mencionados na publicação                   | List[str]    |
| externalLink  | URLs de conteúdo mencionado externo à plataforma              | List[str]    |
| repliedBy     | Nomes de usuários que responderam à publicação                | List[str]    |
| urls          | URLs mencionadas na publicação                                | List[str]    |
| hashtags      | Hashtags usadas na publicação                                 | List[str]    |
| thread        | O conteúdo completo de uma sequência de tweets (Twitter thread) | str          |
