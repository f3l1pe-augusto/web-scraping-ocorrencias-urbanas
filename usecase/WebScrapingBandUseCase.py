import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def scrape_news_band(url, search_term, log):
    driver = configure_driver()
    try:
        html_content = load_page(driver, url, log)
        parse_news(html_content, search_term, log)
    finally:
        driver.quit()


def configure_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def load_page(driver, url, log, max_clicks=15):
    driver.get(url)
    log.info(f"Título da página: {driver.title}")
    log.info("Carregando notícias...")

    for _ in range(max_clicks):
        try:
            driver.execute_script("window.scrollBy(0, 3000);")
            load_more_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Carregar mais')]")
            load_more_button.click()
            time.sleep(1)
        except Exception as e:
            log.error(f"Ocorreu um erro ao carregar a página: {e}")
            break

    return driver.page_source


def parse_news(html_content, search_term, log):
    soup = BeautifulSoup(html_content, 'lxml')
    all_news = soup.find_all('div', class_='box-cards')

    log.info(f"Ocorrências sobre {search_term}")

    count = 0
    for index, single_news in enumerate(all_news, start=1):
        news_title = single_news.find('h2', class_="title").text
        published_date = single_news.find('time', class_='published').text
        link = single_news.find('a', class_='link')['href']

        if search_term.lower() in news_title.lower() and "bauru" in news_title.lower():
            count += 1
            log.info(f"Notícia {count}: {news_title.strip()}")
            log.info(f"Data da publicação: {published_date}")
            log.info(f"Link da reportagem: {link}")

    if count == 0:
        log.info("Nenhuma notícia recente encontrada para o termo de pesquisa.")
