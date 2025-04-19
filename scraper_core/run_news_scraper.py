from scraper_core.usecase.GetNewsUseCase import scrape_news
from scraper_core.log.LoggerConfig import LoggerConfig
import os
import pandas as pd
from dotenv import load_dotenv

class ScrapeNewsUseCase:
    def __init__(self):
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()

    def run(self, url, search_term, site, google_maps_api_key):
        return scrape_news(url, search_term, self.logger, site, google_maps_api_key)

def main():
    load_dotenv()

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

    band_news = scrape_news_use_case.run(url_band, search_terms, 'band', api_key)
    g1_news = scrape_news_use_case.run(url_g1, search_terms, 'g1', api_key)
    jcnet_news = scrape_news_use_case.run(url_jcnet, search_terms, 'jcnet', api_key)
    _94fm_news = scrape_news_use_case.run(url_94fm, search_terms, '94fm', api_key)

    band_df = pd.DataFrame(band_news)
    g1_df = pd.DataFrame(g1_news)
    jcnet_df = pd.DataFrame(jcnet_news)
    _94fm_df = pd.DataFrame(_94fm_news)

    df_all_news = pd.concat([band_df, g1_df, jcnet_df, _94fm_df], ignore_index=True)


    os.makedirs('scraper_core/data', exist_ok=True)

    df_all_news_path = 'scraper_core/data/df_all_news.csv'

    pd.DataFrame(df_all_news).to_csv(df_all_news_path, index=False)

    scrape_news_use_case.logger.info(f"Notícias salvas em: {df_all_news_path}")

if __name__ == "__main__":
    main()
