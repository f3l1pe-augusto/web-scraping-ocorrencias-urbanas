import subprocess
import sys


def main():
    print("=== Web Scraping Ocorrências Urbanas ===")
    print("1 - Scraping de sites de notícias (G1, Band, JCNet e 94FM)")
    print("2 - Scraping de redes sociais (X)")
    print("0 - Sair")

    choice = input("Escolha uma opção: ")

    if choice == "1":
        subprocess.run([sys.executable, "scraper_core/run_news_scraper.py"])
    elif choice == "2":
        print("Módulo de redes sociais ainda não implementado.")
    elif choice == "0":
        print("Encerrando o programa.")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
