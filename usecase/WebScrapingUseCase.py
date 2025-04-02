import time

import dateparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from unidecode import unidecode

from util.Util import get_ceps, get_coordinates, extract_addresses, remove_semicolons, remove_duplicate_spaces

NUM_CLICKS = 10 # Número de cliques na página para carregar mais notícias

def configure_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(options=options)

def load_page(driver, url, log, clicks=NUM_CLICKS):
    driver.get(url)
    log.info(f"Título da página: {driver.title}")
    log.info("Carregando notícias...")

    for click in range(clicks):
        try:
            driver.execute_script("window.scrollBy(0, 20000);")
            if "band.uol" in driver.current_url:
                load_more_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Carregar mais')]")
            elif "g1.globo" in driver.current_url:
                close_cookie_banner_g1(driver, log)
                load_more_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Veja mais')]")
            elif "sampi.net" in driver.current_url:
                break
            else:
                continue

            if load_more_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button[0])
                driver.execute_script("arguments[0].click();", load_more_button[0])
                log.info(f"Carregando mais notícias... Aguarde... Click: {click + 1}")
                time.sleep(2)
            else:
                log.info("Botão para carregar a página não encontrado.")
                break
        except Exception as e:
            log.error(f"Ocorreu um erro ao carregar a página: {e}")
            break

    return driver.page_source

def fetch_wayback_snapshot(url, timestamp=None):
    base_url = "http://archive.org/wayback/available"
    params = {"url": url}
    if timestamp:
        params["timestamp"] = timestamp

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        snapshots = data.get("archived_snapshots", {})
        if "closest" in snapshots:
            return snapshots["closest"]
        else:
            return None
    else:
        return None

def close_cookie_banner_g1(driver, log):
    try:
        cookie_banner = driver.find_element(By.XPATH, "//*[contains(text(), 'Prosseguir')]")
        cookie_banner.click()
    except Exception as e:
        log.info(f"Banner de cookies não encontrado ou aceito: {e}")

def get_jcnet_date(driver, link, log):
    try:
        driver.get(link)
        time.sleep(2)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'lxml')

        date_element = soup.find('time')
        date = date_element['datetime'] if date_element and date_element.has_attr('datetime') else "Data não encontrada"

        return date
    except Exception as e:
        log.error(f"Erro ao recuperar a data da notícia: {e}")
        return "Data não encontrada"

def get_band_subtitle(driver, link, log):
    try:
        driver.get(link)
        time.sleep(2)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'lxml')

        subtitle = soup.find('h2', class_='subtitle').text if soup.find('h2', class_='subtitle') else "Subtítulo não encontrado"

        return subtitle
    except Exception as e:
        log.error(f"Erro ao recuperar o subtítulo da notícia: {e}")
        return "Subtítulo não encontrado"

def get_news_content(driver, link, log):
    try:
        driver.get(link)
        time.sleep(2)
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'lxml')

        if "band.uol" in link:
            content = ' '.join([
                p.text
                for p in soup.find_all('p')
                if 'author__name' not in p.get('class', [])
                   and 'Band Multi' not in p.text
                   and 'Siga a Band Multi nas redes' not in p.text
                   and 'Band.com.br' not in p.text
                   and 'Siga a Band.com.br nas redes' not in p.text
                   and 'Utilizamos cookies essenciais e tecnologias semelhantes de acordo com a nossa Política de Privacidade e, ao continuar navegando, você concorda com estas condições.' not in p.text
                   and 'Bauru e Marília' not in p.text
                   and 'Por Hiltonei Fernando' not in p.text
                   and 'Nos siga nas redes sociais Por Hiltonei Fernando' not in p.text
                   and 'Li e concordo com os Termos de Uso e Políticas de Privacidade' not in p.text])
        elif "g1.globo" in link:
            content = ' '.join([
                p.text
                for p in soup.find_all('p', class_='content-text__container')
                if '📲 Participe do canal do g1 Bauru e Marília no WhatsApp' not in p.text
                   and 'Veja mais notícias da região no g1 Bauru e Marília' not in p.text])
        elif "sampi.net" in link:
            content = ' '.join([
                p.text
                for p in soup.find_all('p')
                if 'Receba as notícias mais relevantes de Bauru e região direto no seu whatsapp. Participe da Comunidade' not in p.text
                   and 'JCNET integra a maior rede de notícias do interior.' not in p.text
                   and 'Notícias que importam onde você estiver' not in p.text
                   and 'mb-1' not in p.get('class', [])
                   and 'text-laranja' not in p.get('class', [])])
        else:
            log.error("Site não suportado para extração de conteúdo")
            return "Conteúdo não disponível"

        return content.strip()
    except Exception as e:
        log.error(f"Erro ao recuperar o conteúdo da notícia: {e}")
        return "Erro ao recuperar o conteúdo"

def parse_news(html_content, search_terms, log, site, driver, google_maps_api_key):
    soup = BeautifulSoup(html_content, 'lxml')

    if site == 'band':
        all_news = soup.find_all('div', class_='box-cards')
    elif site == 'g1':
        all_news = soup.find_all('div', class_='feed-post-body')
    elif site == 'jcnet':
        all_news = soup.find_all('div', class_='col-24')
    else:
        log.error("Site não suportado")
        return []

    log.info(f"Buscando ocorrências que contenham qualquer um dos termos: {search_terms}")

    # Se search_terms for uma ‘string’, transforma-a numa lista com um único elemento
    if isinstance(search_terms, str):
        search_terms = [search_terms]

    # Normaliza os termos de busca (assegura que não sejam iterados caractere a caractere)
    normalized_search_terms = [unidecode(term.lower()) for term in search_terms]

    news_list = []
    for index, single_news in enumerate(all_news, start=1):
        try:
            if site == 'band':
                title = single_news.find('h2', class_='title').text if single_news.find('h2', class_='title') else "Título não encontrado"
                subtitle = ''
                link = single_news.find('a', class_='link')['href'] if single_news.find('a', class_='link') else "#"
                published_date = single_news.find('time', class_='published').text if single_news.find('time', class_='published') else "Data não encontrada"
            elif site == 'g1':
                title = single_news.find('p', {'elementtiming': 'text-csr'}).text if single_news.find('p', {'elementtiming': 'text-csr'}) else "Título não encontrado"
                subtitle = single_news.find('div', class_='feed-post-body-resumo').text if single_news.find('div', class_='feed-post-body-resumo') else "Subtítulo não encontrado"
                link = single_news.find('a', class_='feed-post-link')['href'] if single_news.find('a', class_='feed-post-link') else "#"
                published_date = single_news.find('span', class_='feed-post-datetime').text if single_news.find('span', class_='feed-post-datetime') else "Data não encontrada"
            elif site == 'jcnet':
                title = single_news.find('h3', class_='mb-0').text if single_news.find('h3', class_='mb-0') else "Título não encontrado"
                subtitle = ''
                link = single_news.find('a', class_='hoverActive')['href'] if single_news.find('a', class_='hoverActive') else "#"
                published_date = ''
            else:
                log.error("Site não suportado")
                return []

            # Normalização para comparações (tudo em minúsculo e sem acentos)
            title_normalized = unidecode(title.lower())

            subtitle_normalized = unidecode(subtitle.lower())

            # Verifica se a notícia contém pelo menos um dos termos informados (no título ou subtítulo)
            search_term = next((term for term in normalized_search_terms if term in title_normalized or term in subtitle_normalized), None)

            # Verifica se a notícia menciona a cidade de Bauru (no título ou subtítulo)
            bauru = "bauru" in title_normalized or "bauru" in subtitle_normalized

            # Apenas adiciona a notícia se atender a ambos os critérios
            if search_term and bauru:
                if site == 'jcnet':
                    published_date = get_jcnet_date(driver, link, log)

                parsed_date = dateparser.parse(published_date)
                if parsed_date:
                    published_date = parsed_date.strftime('%d/%m/%Y')
                else:
                    published_date = "Data não encontrada"

                if site == 'band':
                    subtitle = get_band_subtitle(driver, link, log)

                content = get_news_content(driver, link, log)
                addresses, address_types = extract_addresses(content, log)
                ceps = get_ceps(addresses, google_maps_api_key, log)
                coordinates = get_coordinates(ceps, addresses, google_maps_api_key, log)

                content = remove_duplicate_spaces(content)
                content = remove_semicolons(content)
                title = remove_duplicate_spaces(title)
                title = remove_semicolons(title)
                subtitle = remove_duplicate_spaces(subtitle)
                subtitle = remove_semicolons(subtitle)

                if coordinates:
                    news_list.append({
                        'title': title,
                        'subtitle': subtitle,
                        'content': content,
                        'published_date': published_date,
                        'link': link,
                        'address_types': address_types,
                        'coordinates': coordinates,
                        'site': site,
                        'search_term': search_term
                    })

        except Exception as e:
            log.error(f"Erro ao processar notícia {index}: {e}")
            continue

    if not news_list:
        log.info(f"Nenhuma notícia encontrada para os termos de pesquisa no site {site}.")

    return news_list

def scrape_archived_news(url, timestamp, search_term, log, site, google_maps_api_key):
    snapshot = fetch_wayback_snapshot(url, timestamp)
    if not snapshot or not snapshot.get("available", False):
        log.warning(f"Nenhum snapshot disponível para {url} em {timestamp}.")
        return []

    archived_url = snapshot["url"]
    log.info(f"Snapshot encontrado: {archived_url}")
    return scrape_news(archived_url, search_term, log, site, google_maps_api_key)

def scrape_news(url, search_terms, log, site, google_maps_api_key):
    driver = configure_driver()
    try:
        html_content = load_page(driver, url, log)

        # Criar um conjunto para armazenar notícias únicas
        all_news = []
        seen_titles = set()

        log.info(f"Buscando notícias sobre os termos {search_terms} no site {site}...")
        news_list = parse_news(html_content, search_terms, log, site, driver, google_maps_api_key)

        for news in news_list:
            if news['title'] not in seen_titles:
                all_news.append(news)
                seen_titles.add(news['title'])

        return all_news
    finally:
        driver.quit()
        log.info("Driver fechado com sucesso.")
