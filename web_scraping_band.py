from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_news(url):
    options = Options()
    options.add_argument("--headless") # Executa o navegador em segundo plano
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    print("\n" + driver.title + "\n")

    print("Carregando notícias...\n")

    click = 0 # Contador de cliques no botão "Carregar mais"
    while True:
        if click == 10:
            break

        driver.execute_script("window.scrollBy(0, 2000);") # Scroll down

        element = driver.find_element(By.CSS_SELECTOR, 'span.button') # Botão "Carregar mais"
        element.click()

        click += 1

        time.sleep(1) # Aguarda 1 segundo para os elementos da página renderizarem

    html_content = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html_content, 'lxml')
    all_news = soup.find_all('div', class_='box-cards')

    occurrence = input("Digite uma cidade ou ocorrência pela qual deseja filtrar (Bauru, Marília, roubo): ")

    print("\nOcorrências sobre " + occurrence + "\n")

    count = 0
    for index, single_news in enumerate(all_news, start=1):
        news_title = single_news.find('h2', class_="title").text
        published_date = single_news.find('time', class_='published').text
        link = single_news.find('a', class_='link')['href']

        if occurrence.lower() in news_title.lower():
            count += 1
            print(f"Notícia {count}: {news_title.strip()}\n")
            print(f"Data da publicação: {published_date}\n")
            print(f"Link da reportagem: {link}\n")

    if count == 0:
        print("Não há registros recentes.")

if __name__ == "__main__":
    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    scrape_news(url_band)
