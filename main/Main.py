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

    # url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    url_g1 = 'https://g1.globo.com/sp/bauru-marilia/'
    # url_jcnet = 'https://sampi.net.br/bauru'

    occurrences = input("Digite as ocorrências (separadas por vírgula) pela qual deseja filtrar (ex: roubo, furto, falta de luz): ")
    search_terms = [term.strip() for term in occurrences.split(",")]

    scrape_news_use_case = ScrapeNewsUseCase()

    # Notícias atuais
    # news_band = scrape_news_use_case.run(url_band, occurrence, 'band', api_key)
    news_g1 = scrape_news_use_case.run(url_g1, search_terms, 'g1', api_key)
    # news_jcnet = scrape_news_use_case.run(url_jcnet, search_terms, 'jcnet', api_key)

    # Notícias de 5 anos atrás
    # timestamp = scrape_news_use_case.get_five_years_ago_date()
    # old_news_band = scrape_archived_news(url_band, timestamp, occurrence, scrape_news_use_case.logger, 'band', api_key)
    # old_news_g1 = scrape_archived_news(url_g1, timestamp, occurrence, scrape_news_use_case.logger, 'g1', api_key)
    # old_news_jcnet = scrape_archived_news(url_jcnet, timestamp, occurrence, scrape_news_use_case.logger, 'jcnet', api_key)

    # Consolidação dos dados
    dataset_g1 = news_g1
    # all_old_news = old_news_band + old_news_g1 + old_news_jcnet

    # Salvar em CSV
    os.makedirs('../data', exist_ok=True)

    dataset_g1_path = '../data/dataset_g1.csv'
    # old_news_path = '../data/old_news_data.csv'

    pd.DataFrame(dataset_g1).to_csv(dataset_g1_path, index=False)
    # pd.DataFrame(all_old_news).to_csv(old_news_path, index=False)

    scrape_news_use_case.logger.info(f"Notícias atuais salvas em: {dataset_g1_path}")
    # scrape_news_use_case.logger.info(f"Notícias antigas salvas em: {old_news_path}")
