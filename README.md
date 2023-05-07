# FSL0302-nitter_search
[![CodeFactor](https://www.codefactor.io/repository/github/hermengardo/fsl0302-nitter_search/badge)](https://www.codefactor.io/repository/github/hermengardo/fsl0302-nitter_search)
[![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

## **Introdução**
- Web scraper desenvolvido para coletar tweets do Nitter.net, um front-end alternativo ao Twitter que oferece aos usuários uma experiência mais segura e privada. O programa é especialmente útil para pesquisadores e analistas de dados que desejam coletar tweets sem depender de uma conta ou da API do Twitter.
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
| `random_interval` | tuple | Intervalo de tempo para o random_time. O padrão é (0, 1), o que significa que um tempo aleatório entre 0 e 1 segundo será adicionado a cada solicitação de coleta (caso `random_time=True`). | Sim |
| `seed` | int | Seed do gerador de números aleatórios. | Sim |

## **Campos disponíveis**

| Variável        | Descrição                                                           |
|--------------------|-----------------------------------------------------------------------|
| fullname           | Nome completo do autor da publicação                                   |
| username           | Nome de usuário do autor da publicação                                 |
| content            | Texto da publicação                                                   |
| publishedAt | Data e hora em que a publicação foi feita                              |
| comments         | Número de comentários na publicação                                    |
| retweets         | Número de retweets da publicação                                       |
| quotes           | Número de citações da publicação                                       |
| hearts           | Número de curtidas/likes da publicação                                 |
| imgAvatar         | Foto de perfil do autor da publicação                                  |
| images             | Imagens incluídas na publicação                                         |
| videos             | Vídeos incluídos na publicação                                         |
| quote              | Links para qualquer tweet citado ou conteúdo externo                   |
| externalLink        | Links para qualquer conteúdo de terceiros mencionado na publicação     |
| repliedBy         | Nomes de usuários que responderam à publicação                          |
| urls               | URLs mencionadas na publicação                                          |
| hashtags           | Hashtags usadas na publicação                                          |
