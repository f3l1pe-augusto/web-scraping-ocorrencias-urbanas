import logging
import time
import colorlog

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors=log_colors
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

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
    logger.info(f"Título da página: {driver.title}")
    logger.info("Carregando notícias...")

    for _ in range(max_clicks):
        try:
            driver.execute_script("window.scrollBy(0, 2000);")
            element = driver.find_element(By.CSS_SELECTOR, 'span.button')
            element.click()
            time.sleep(1)
        except Exception as e:
            logger.error(f"Ocorreu um erro ao carregar a página: {e}")
            break

    return driver.page_source

def parse_news(html_content, search_term):
    soup = BeautifulSoup(html_content, 'lxml')
    all_news = soup.find_all('div', class_='box-cards')

    logger.info(f"Ocorrências sobre {search_term}")

    count = 0
    for index, single_news in enumerate(all_news, start=1):
        news_title = single_news.find('h2', class_="title").text
        published_date = single_news.find('time', class_='published').text
        link = single_news.find('a', class_='link')['href']

        if search_term.lower() in news_title.lower():
            count += 1
            logger.info(f"Notícia {count}: {news_title.strip()}")
            logger.info(f"Data da publicação: {published_date}")
            logger.info(f"Link da reportagem: {link}")

    if count == 0:
        logger.info("Nenhuma notícia recente encontrada para o termo de pesquisa.")

if __name__ == "__main__":
    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    occurrence = input("Digite uma cidade ou ocorrência pela qual deseja filtrar (Bauru, Marília, furto): ")
    scrape_news(url_band, occurrence)
