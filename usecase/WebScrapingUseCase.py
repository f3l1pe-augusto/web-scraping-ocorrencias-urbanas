import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from unidecode import unidecode

MAX = int(os.getenv('MAX_CLICKS', 20))

def configure_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def close_cookie_banner_g1(driver, log):
    try:
        cookie_banner = driver.find_element(By.XPATH, "//*[contains(text(), 'Prosseguir')]")
        cookie_banner.click()
    except Exception as e:
        log.info(f"Banner de cookies não encontrado ou já aceito: {e}")

def load_page(driver, url, log, max_clicks=MAX):
    driver.get(url)
    log.info(f"Título da página: {driver.title}")
    log.info("Carregando notícias...")

    for _ in range(max_clicks):
        try:
            driver.execute_script("window.scrollBy(0, 10000);")
            if "band.uol" in driver.current_url:
                load_more_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Carregar mais')]")
            elif "g1.globo" in driver.current_url:
                close_cookie_banner_g1(driver, log)
                load_more_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Veja mais')]")
            else:
                continue
            load_more_button.click()
            time.sleep(2)
        except Exception as e:
            log.error(f"Ocorreu um erro ao carregar a página: {e}")
            break

    return driver.page_source


def get_news_content(driver, link, log):
    try:
        driver.get(link)
        time.sleep(2)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'lxml')

        if "band.uol" in link:
            content = soup.find('h2', class_='subtitle').text
        elif "g1.globo" in link:
            content = soup.find('h2', class_='content-head__subtitle').text
        elif "sampi.net" in link:
            content = soup.find('div', class_='texto0 mt-4').text
        else:
            log.error("Site não suportado para extração de conteúdo")
            return "Conteúdo não disponível"

        return content.strip()
    except Exception as e:
        log.error(f"Erro ao recuperar o conteúdo da notícia: {e}")
        return "Erro ao recuperar o conteúdo"

def parse_news(html_content, search_term, log, site, driver):
    soup = BeautifulSoup(html_content, 'lxml')
    if site == 'band':
        all_news = soup.find_all('div', class_='box-cards')
    elif site == 'g1':
        all_news = soup.find_all('div', class_='feed-post-body')
    elif site == 'jcnet':
        all_news = soup.find_all('div', class_='col-8')
    else:
        log.error("Site não suportado")
        return

    log.info(f"Ocorrências sobre {search_term}")
    search_term_normalized = unidecode(search_term.lower())

    count = 0
    for index, single_news in enumerate(all_news, start=1):
        try:
            if site == 'band':
                news_title = single_news.find('h2', class_="title").text \
                    if single_news.find('h2', class_="title") else "Título não encontrado"
                published_date = single_news.find('time', class_='published').text \
                    if single_news.find('time', class_='published') else "Data não encontrada"
                link = single_news.find('a', class_='link')['href'] \
                    if single_news.find('a', class_='link') else "#"
            elif site == 'g1':
                news_title = single_news.find('p', {'elementtiming': 'text-csr'}).text \
                    if single_news.find('p', {'elementtiming': 'text-csr'}) else "Título não encontrado"
                published_date = single_news.find('span', class_='feed-post-datetime').text \
                    if single_news.find('span', class_='feed-post-datetime') else "Data não encontrada"
                link = single_news.find('a', class_='feed-post-link')['href'] \
                    if single_news.find('a', class_='feed-post-link') else "#"
            elif site == 'jcnet':
                news_title = single_news.find('h3').text \
                    if single_news.find('h3') else "Título não encontrado"
                published_date = 'Não disponível'
                link = single_news.find('a', class_='hoverActive')['href'] \
                    if single_news.find('a', class_='hoverActive') else "#"
            else:
                log.error("Site não suportado")
                return

            news_title_normalized = unidecode(news_title.lower())
            if search_term_normalized in news_title_normalized and "bauru" in news_title_normalized:
                count += 1
                log.info(f"Notícia {count}: {news_title.strip()}")
                log.info(f"Data da publicação: {published_date}")
                log.info(f"Link da reportagem: {link}")

                content = get_news_content(driver, link, log)
                log.info(f"Conteúdo da notícia: {content}")

        except Exception as e:
            log.error(f"Erro ao processar notícia {index}: {e}")
            continue

    if count == 0:
        log.info(f"Nenhuma notícia recente encontrada para o termo de pesquisa no site {site}.")

def scrape_news(url, search_term, log, site):
    driver = configure_driver()
    try:
        html_content = load_page(driver, url, log)
        parse_news(html_content, search_term, log, site, driver)
    finally:
        driver.quit()
        log.info("Driver fechado com sucesso.")
