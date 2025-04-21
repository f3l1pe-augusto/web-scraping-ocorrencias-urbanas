# Web Scraping de Ocorrências Urbanas

Este projeto faz parte de uma iniciação científica feita na Unesp Bauru, que visa fazer um levantamento de ocorrências urbanas que acontecem na cidade de Bauru-SP, utilizando como fonte de dados vários portais de notícias locais e redes sociais. Para isso, foram utilizadas técnicas de computação e ciência de dados com intuito de identificar informações e dados relevantes que indiquem tais ocorrências. Os dados foram extraídos utilizando a linguagem Python e as bibliotecas BeautifulSoup, Selenium e Twikit, as ocorrências extraídas em arquivos CSV serão utilizadas para análise posterior. Após analisar os dados, o objetivo final será a disponibilização do conjunto de dados coletado e a criação de um Sistema de Informação Geográfica (SIG) que permita visualizar as ocorrências urbanas num mapa da cidade de Bauru, com o intuito de auxiliar tomadas de decisões baseadas em dados.

## Menu inicial

![img.png](images/img.png)

## Sites suportados

- [G1 Bauru](https://g1.globo.com/sp/bauru-marilia/)
- [Band Bauru](https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias)
- [94 FM](https://www.94fm.com.br/noticias/)

## Redes sociais suportadas

- [X (Twitter)](https://x.com/)

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/f3l1pe-augusto/web-scraping-ocorrencias-urbanas.git
    cd web-scraping-ocorrencias-urbanas
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Execute o script `Main.py`:
    ```sh
    python Main.py
    ```

2. Escolha uma das opções do menu:
    - `1` para fazer scraping de notícias
    - `2` para fazer scraping de redes sociais
    - `0` para sair do programa

3. Siga as instruções na tela para realizar o scraping.

4. Os dados extraídos pelo scraper de notícias serão salvos num arquivo CSV na pasta `scraper_core/data/`, enquanto os dados extraídos pelo scraper de redes sociais serão salvos na pasta `social_scraper/data/`.

## Estrutura do Projeto

```plaintext
web-scraping-ocorrencias-urbanas/
├── Main.py                         # Script principal com menu de execução
├── requirements.txt                # Lista de dependências do projeto
├── README.md                       # Documentação do projeto
├── LICENSE                         # Licença de uso
├── images/                         # Pasta com as imagens do projeto
│   ├── img.png                     # Imagem do menu inicial
├── scraper_core/                   # Módulo principal de scraping de notícias
│   ├── __init__.py
│   ├── run_news_scraper.py         # Executa o processo de scraping de notícias
│   ├── log/
│   │   ├── __init__.py
│   │   └── LoggerConfig.py         # Configuração de logs para monitoramento e debug
│   ├── usecase/
│   │   ├── __init__.py
│   │   └── GetNewsUseCase.py      # Caso de uso principal para scraping dos portais de notícias
│   └── util/
│       ├── __init__.py
│       └── Util.py                # Funções utilitárias para o projeto (limpeza, formatação, extração de coordenadas, etc)
└── social_scraper/                # Estrutura inicial para scraping de redes sociais
    ├── __init__.py
    ├── run_social_scraper.py      # Executa o processo de scraping de redes sociais
    ├── config/
    │   └── config.py              # Configuração das credenciais do X (Twitter)
    ├── usecase/
    │   ├── __init__.py
    │   └── GetTweetsUseCase.py    # Caso de uso principal para scraping das redes sociais
```

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch: `git checkout -b minha-nova-feature`
3. Faça as suas alterações e commit: `git commit -am 'Adiciona nova feature'`
4. Envie para o repositório remoto: `git push origin minha-nova-feature`
5. Abra um Pull Request.

## Observações

### ChromeDriver

Para o scraping em portais de notícias locais são usados o navegador Google Chrome e o ChromeDriver baixe o [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br) e adicione o caminho para o arquivo executável ao seu PATH.

### Twikit

O projeto utiliza a biblioteca gratuita e de código aberto [Twikit](https://github.com/d60/twikit) para realizar scraping na rede social X (Twitter). Para instalar a biblioteca, utilize o seguinte comando:

```sh
pip install twikit
 ```

### Google Geocoding API

Esse projeto utiliza a Google Geocoding API para converter endereços em coordenadas geográficas. Para utilizar essa funcionalidade, você precisará de uma chave de API do Google. Siga as instruções [aqui](https://developers.google.com/maps/documentation/geocoding/get-api-key) para obter a sua chave.

Após obter a chave, você deve adicioná-la ao arquivo .env na raiz do projeto, com o seguinte formato:

```plaintext
GOOGLE_MAPS_API_KEY=sua_chave_aqui
```

### Mudanças na Estrutura HTML das páginas

As páginas web podem alterar a sua estrutura HTML ao longo do tempo, o que pode ocasionar erros no scraper. Caso isso ocorra, será necessário atualizar o código para refletir as novas mudanças na estrutura das páginas. Fique atento a possíveis falhas na extração de dados e reveja o código conforme necessário.

### Política de acesso a dados do X (Twitter)

A rede social X (Twitter) pode alterar as suas políticas de acesso e scraping, o que pode afetar a funcionalidade do scraper. Esteja ciente de que o uso de scraping em redes sociais pode violar os Termos de Serviço da plataforma. É recomendável revir as políticas de uso da X (Twitter) antes de utilizar o scraper.

### Aviso Legal

Este projeto foi desenvolvido apenas para fins educacionais e não deve ser utilizado para coletar dados de sites e redes sociais sem a permissão dos seus proprietários. O uso indevido deste projeto é de responsabilidade do usuário.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
