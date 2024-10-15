from usecase.WebScrapingUseCase import scrape_news
from log.LoggerConfig import LoggerConfig

class ScrapeNewsUseCase:
    def __init__(self):
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()

    def run(self, url, search_term, site):
        scrape_news(url, search_term, self.logger, site)

if __name__ == "__main__":
    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    url_g1 = 'https://g1.globo.com/sp/bauru-marilia/'
    url_jcnet = 'https://sampi.net.br/bauru'
    occurrence = input("Digite uma ocorrência pela qual deseja filtrar na cidade de Bauru (ex: roubo, furto, falta de luz ou água): ")

    scrape_news_use_case = ScrapeNewsUseCase()
    scrape_news_use_case.run(url_band, occurrence, 'band')
    scrape_news_use_case.run(url_g1, occurrence, 'g1')
    scrape_news_use_case.run(url_jcnet, occurrence, 'jcnet')
