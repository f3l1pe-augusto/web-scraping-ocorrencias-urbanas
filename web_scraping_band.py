import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_news(url, search_term):
    driver = configure_driver()
    try:
        html_content = load_page(driver, url)
        parse_news(html_content, search_term)
    finally:
        driver.quit()

def configure_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def load_page(driver, url, max_clicks=20):
    driver.get(url)
    logging.info(f"Título da página: {driver.title}")
    logging.info("Carregando notícias...")

    for click in range(max_clicks):
        try:
            driver.execute_script("window.scrollBy(0, 2000);")
            element = driver.find_element(By.CSS_SELECTOR, 'span.button')
            element.click()
            time.sleep(1)
        except Exception as e:
            logging.error(f"Ocorreu um erro ao carregar a página: {e}")
            break

    return driver.page_source

def parse_news(html_content, search_term):
    soup = BeautifulSoup(html_content, 'lxml')
    all_news = soup.find_all('div', class_='box-cards')

    logging.info(f"Ocorrências sobre {search_term}")

    count = 0
    for index, single_news in enumerate(all_news, start=1):
        news_title = single_news.find('h2', class_="title").text
        published_date = single_news.find('time', class_='published').text
        link = single_news.find('a', class_='link')['href']

        if search_term.lower() in news_title.lower():
            count += 1
            logging.info(f"Notícia {count}: {news_title.strip()}")
            logging.info(f"Data da publicação: {published_date}")
            logging.info(f"Link da reportagem: {link}")

    if count == 0:
        logging.info("Não há registro recentes.")

if __name__ == "__main__":
    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    occurrence = input("Digite uma cidade ou ocorrência pela qual deseja filtrar (Bauru, Marília, furto): ")
    scrape_news(url_band, occurrence)
