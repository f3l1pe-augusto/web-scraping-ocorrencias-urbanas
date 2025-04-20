import subprocess
import sys

def main():
    print("=== Web Scraping de Ocorrências Urbanas na cidade de Bauru ===")
    print("1 - Scraping de sites de notícias (G1, Band e 94FM)")
    print("2 - Scraping de redes sociais (X)")
    print("0 - Sair")

    choice = input("Escolha uma opção: ")

    if choice == "1":
        subprocess.run([sys.executable, "scraper_core/run_news_scraper.py"])
    elif choice == "2":
        subprocess.run([sys.executable, "social_scraper/run_social_scraper.py"])
    elif choice == "0":
        print("Encerrando o programa.")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
