from usecase.WebScrapingUseCase import scrape_news, scrape_archived_news
from log.LoggerConfig import LoggerConfig
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

class ScrapeNewsUseCase:
    def __init__(self):
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()

    @staticmethod
    def get_five_years_ago_date():
        today = datetime.now()
        five_years_ago = today - timedelta(days = 5 * 365)
        return five_years_ago.strftime('%Y%m%d')

    def run(self, url, search_term, site, google_maps_api_key):
        return scrape_news(url, search_term, self.logger, site, google_maps_api_key)

if __name__ == "__main__":
    load_dotenv()  # Carrega as variáveis do arquivo .env

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("A variável GOOGLE_MAPS_API_KEY não está definida no arquivo .env.")

    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    url_g1 = 'https://g1.globo.com/sp/bauru-marilia'
    url_jcnet = 'https://sampi.net.br/bauru'
    url_94fm = "https://www.94fm.com.br/noticias/"

    occurrences = input("Digite as ocorrências (separadas por vírgula) pela qual deseja filtrar (ex: roubo, furto, falta de luz): ")
    search_terms = [term.strip() for term in occurrences.split(",")]

    scrape_news_use_case = ScrapeNewsUseCase()

    # Notícias atuais
    # band_news = scrape_news_use_case.run(url_band, search_terms, 'band', api_key)
    # g1_news = scrape_news_use_case.run(url_g1, search_terms, 'g1', api_key)
    # jcnet_news = scrape_news_use_case.run(url_jcnet, search_terms, 'jcnet', api_key)
    _94fm_news = scrape_news_use_case.run(url_94fm, search_terms, '94fm', api_key)

    # Notícias de 5 anos atrás
    # timestamp = scrape_news_use_case.get_five_years_ago_date()
    # old_band_news = scrape_archived_news(url_band, timestamp, search_terms, scrape_news_use_case.logger, 'band', api_key)
    # old_g1_news = scrape_archived_news(url_g1, timestamp, search_terms, scrape_news_use_case.logger, 'g1', api_key)
    # old_jcnet_news = scrape_archived_news(url_jcnet, timestamp, search_terms, scrape_news_use_case.logger, 'jcnet', api_key)

    # Consolidação dos dados
    dataset_94fm_news = _94fm_news
    # dataset_old_g1_news = old_g1_news

    # Salvar em CSV
    os.makedirs('../data', exist_ok=True)

    dataset_94fm_news_path = '../data/dataset_94fm_news.csv'
    # dataset_old_g1_news_path = '../data/dataset_old_g1_news.csv'

    pd.DataFrame(dataset_94fm_news).to_csv(dataset_94fm_news_path, index=False)
    # pd.DataFrame(dataset_old_g1_news).to_csv(dataset_old_g1_news_path, index=False)

    scrape_news_use_case.logger.info(f"Notícias atuais salvas em: {dataset_94fm_news_path}")
    # scrape_news_use_case.logger.info(f"Notícias antigas salvas em: {dataset_old_g1_news_path}")
