# Web Scraping de Notícias

Este projeto realiza a extração de notícias dos sites da Band UOL, G1 Globo e JCNET Sampi na cidade de Bauru utilizando as bibliotecas BeautifulSoup e Selenium, e salva as notícias extraídas em um arquivo CSV para análise posterior.

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

2. Insira as ocorrências pela qual deseja filtrar as notícias quando solicitado pelo script. 

3. As notícias filtradas serão salvas automaticamente em um arquivo CSV na pasta `data`, permitindo análise posterior dos dados extraídos.

## Estrutura do Projeto

- `main`: Script principal do projeto, responsável por executar o programa.
- `usecase`: Contém a lógica de negócio do projeto e é responsável por orquestrar as operações de extração de notícias.
- `log`: Contém o arquivo de configurações de log do projeto que registra as operações realizadas.
- `data`: Diretório onde contém o arquivo CSV no qual as notícias extraídas serão salvas.
- `util`: Diretório que contem funções úteis para o projeto que podem ser usadas em outras classes.
- `requirements.txt`: Lista de dependências do projeto.
- `README.md`: Documentação do projeto.
- `.gitignore`: Usado para ignorar arquivos e pastas desnecessárias no controle de versão.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-nova-feature`
3. Faça suas alterações e commit: `git commit -am 'Adiciona nova feature'`
4. Envie para o repositório remoto: `git push origin minha-nova-feature`
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
