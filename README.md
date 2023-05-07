# **Introdução**
- Web scraper desenvolvido para coletar tweets do Nitter.net, um front-end alternativo ao Twitter que oferece aos usuários uma experiência mais segura e privada. O programa é especialmente útil para pesquisadores e analistas de dados que desejam coletar tweets sem depender de uma conta ou da API do Twitter.
- Desenvolvido para a matéria de Práticas de Pesquisa em Sociologia (USP/2023).

# **Instalação**
1. Clone o repositório:
```sh
git clone https://github.com/hermengardo/FSL0302-nitter_search.git
```

2. Instale as dependências:
```sh
pip install -r requirements.txt
```

3. Edite e execute o arquivo `main.py`.

## Exemplo de uso

```python
from scraper import NitterSearch

def main():
    NitterSearch(query='sua_query')


if __name__ == "__main__":
    main()
```

# **Parâmetros**
Aqui está a tabela atualizada com a informação de quais parâmetros são opcionais na classe `NitterSearch`:

| Parâmetro | Tipo | Descrição | Opcional |
| --- | --- | --- | --- |
| `query` | str | A consulta usada para buscar tweets. | Não |
| `file_path` | str | O caminho do arquivo onde os tweets coletados serão salvos. O padrão é 'data.csv'. | Sim |
| `delay` | float | O tempo de espera em segundos entre as solicitações de coleta de tweets. O padrão é 0,01 segundos. | Sim |
| `random_time` | bool | Um valor booleano que indica se deve ser adicionado um tempo aleatório entre as solicitações. O padrão é `False`. | Sim |
| `random_interval` | tuple | O intervalo de tempo em segundos para adicionar a cada solicitação de coleta de tweets. O padrão é (0, 1), o que significa que um tempo aleatório entre 0 e 1 segundo será adicionado a cada solicitação de coleta de tweets (caso `random_time=True`). | Sim |
| `seed` | int | Seed do gerador de números aleatórios. | Sim |

# **Campos disponíveis**

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
