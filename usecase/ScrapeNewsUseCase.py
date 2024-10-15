from usecase.WebScrapingBandUseCase import scrape_news_band
from log.LoggerConfig import LoggerConfig


def execute(url, search_term, log):
    scrape_news_band(url, search_term, log)


class ScrapeNewsUseCase:
    def __init__(self):
        self.logger_config = LoggerConfig()
        self.logger = self.logger_config.get_logger()

    def run(self, url, search_term):
        execute(url, search_term, self.logger)


if __name__ == "__main__":
    url_band = 'https://www.band.uol.com.br/band-multi/bauru-e-marilia/noticias'
    occurrence = (input("Digite uma ocorrência pela qual deseja filtrar na cidade de Bauru (ex: roubo, furto, falta de luz ou água): "))

    scrape_news_use_case = ScrapeNewsUseCase()
    logger = scrape_news_use_case.logger
    scrape_news_band(url_band, occurrence, logger)
