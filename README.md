# Web Scraping de Notícias

Este projeto realiza a extração de notícias de diversos sites na cidade de Bauru utilizando as bibliotecas BeautifulSoup e Selenium.

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

1. Execute o script `Main.py`:
    ```sh
    python Main.py
    ```

2. Insira a ocorrência pela qual deseja filtrar as notícias quando solicitado pelo script.

## Estrutura do Projeto

- `README.md`: Documentação do projeto.
- `WebScrapingUseCase.py`: Script que executa a extração de notícias dos sites Band, G1 e JCNET.
- `Main.py`: Classe principal que contém a função main.
- `LoggerConfig.py`: Classe  que contém a classe `Log` para gerar logs de execução.
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
