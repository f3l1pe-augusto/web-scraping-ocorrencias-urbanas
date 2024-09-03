# Web Scraping de Notícias da Band

Este projeto realiza a extração de notícias do site da Band da região de Bauru e Marília utilizando as bibliotecas BeautifulSoup e Selenium.

## Requisitos

- Python 3.x
- Google Chrome
- ChromeDriver

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/f3l1pe-augusto/web-scraping-noticias.git
    cd web-scraping-noticias
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

4. Baixe o [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br) e adicione o caminho para o arquivo executável ao seu PATH.

## Uso

1. Execute o script `WebScrapingBand.py`:
    ```sh
    python WebScrapingBand.py
    ```

2. Insira a cidade ou ocorrência pela qual deseja filtrar as notícias quando solicitado pelo script.

## Estrutura do Projeto

- `web_scraping_band.py`: Script principal que executa a função `scrape_news`, responsável pela extração das notícias.
- `requirements.txt`: Lista de dependências do projeto.
- `.gitignore`: Usado para ignorar arquivos e pastas desnecessárias no controle de versão.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-nova-feature`
3. Faça suas alterações e commit: `git commit -am 'Adiciona nova feature'`
4. Envie para o repositório remoto: `git push origin minha-nova-feature`
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
