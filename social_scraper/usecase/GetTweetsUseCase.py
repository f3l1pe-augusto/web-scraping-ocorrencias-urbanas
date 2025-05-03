import os
import time
import csv
from twikit import Client, TooManyRequests
from twikit.errors import TwitterException
from datetime import datetime
from configparser import ConfigParser, NoSectionError, NoOptionError
from random import randint

MINIMUM_TWEETS = 1000
COOKIES = 'cookies.json'
QUERY = 'bauru (roubo OR roubado OR roubada OR furto OR furtado OR furtada OR luz OR energia OR iluminação OR água OR buraco OR calçada OR semáforo OR radar OR árvore OR esgoto OR crime OR criminoso OR criminosa OR assalto OR assaltante OR alagamento OR poste OR enchente OR enxurrada OR queimada OR cratera OR preso OR presa OR interditado OR interdição OR pavimento OR asfalto OR erosão OR dengue OR estupro OR violência OR morre OR morte OR morto OR morta OR obra OR reparo OR baleado OR baleada OR trânsito OR acidente OR temporal OR tempestade OR polícia OR chuva OR crime OR dae OR emdurb OR agressão OR cpfl OR assédio OR prisão OR upa OR ubs OR hospital OR ônibus OR pedofilia OR homicídio OR operação OR delegacia OR samu OR tráfico OR traficante OR droga OR maconha OR cocaína OR crack OR fogo OR fumaça OR poluição OR lixo OR cobra OR escorpião OR abuso OR incêndio OR matar OR matou OR agredida OR agredido OR transporte OR bandido OR interrupção OR corpo OR entulho OR descarte OR abandonado OR feminicídio OR bombeiro OR queda OR batida OR atropelamento OR congestionamento OR reclamação OR reclamam OR barulho OR prefeitura OR sinalização OR desabamento OR desmoronamento OR deslizamento OR falta de OR carro OR moto OR pedestre OR caminhão OR bicicleta) lang:pt until:2025-05-02 since:2020-01-01'
SEARCH_TERMS = [
    'roubo', 'roubado', 'roubada', 'furto', 'furtado', 'furtada', 'luz', 'energia', 'iluminação', 'água', 'buraco', 'calçada',
    'semáforo', 'radar', 'árvore', 'esgoto', 'crime', 'criminoso', 'criminosa', 'assalto', 'assaltante',
    'alagamento', 'poste', 'enchente', 'enxurrada', 'queimada', 'cratera', 'preso',
    'presa', 'interditado', 'interdição', 'pavimento', 'asfalto', 'erosão', 'dengue',
    'estupro', 'violência', 'morre', 'morte', 'morto', 'morta', 'obra', 'reparo', 'baleado', 'baleada', 'trânsito',
    'acidente', 'temporal', 'tempestade', 'polícia', 'chuva', 'crime', 'dae',
    'emdurb', 'agressão', 'cpfl', 'assédio', 'prisão', 'upa', 'ubs', 'hospital', 'ônibus',
    'pedofilia', 'homicídio', 'operação', 'delegacia', 'samu', 'tráfico', 'traficante', 'droga', 'maconha', 'cocaína', 'crack',
    'fogo', 'fumaça', 'poluição', 'lixo', 'cobra', 'escorpião', 'abuso', 'incêndio', 'matar', 'matou'
    'agredida', 'agredido', 'transporte', 'bandido', 'interrupção', 'corpo',
    'entulho', 'descarte', 'abandonado', 'feminicídio', 'bombeiro', 'queda',
    'batida', 'atropelamento', 'congestionamento', 'reclamação', 'reclamam', 'barulho', 'prefeitura', 'sinalização',
    'desabamento', 'desmoronamento', 'deslizamento', 'falta de', 'carro', 'moto', 'pedestre', 'bicicleta', 'caminhão',
]

async def get_tweets(tweets):
    if tweets is None:
        print(f"{datetime.now()} - Carregando tweets...")
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f"{datetime.now()} - Carregando próximos tweets depois de {wait_time} segundos...")
        time.sleep(wait_time)
        tweets = await tweets.next()

    return tweets

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.ini'))

if not os.path.exists(config_path):
    raise FileNotFoundError(f"{datetime.now()} - O arquivo config.ini não foi encontrado no caminho: {config_path}")

config = ConfigParser()
try:
    config.read(config_path)
    username = config.get('X', 'username')
    email = config.get('X', 'email')
    password = config.get('X', 'password')
except NoSectionError:
    raise ValueError(f"{datetime.now()} - A seção [X] não foi encontrada no arquivo config.ini. Verifique o conteúdo do arquivo.")
except NoOptionError as e:
    raise ValueError(f"{datetime.now()} - A chave {e.option} não foi encontrada na seção [X] do arquivo config.ini.")

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, 'tweets.csv')

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['tweet_count', 'username', 'text', 'created_at', 'retweets', 'likes'])

client = Client(language='pt-BR')

async def run():
    try:
        if os.path.exists(COOKIES) and os.path.getsize(COOKIES) > 0:
            print(f"{datetime.now()} - Carregando cookies existentes...")
            client.load_cookies(COOKIES)
        else:
            print(f"{datetime.now()} - Realizando login...")
            await client.login(
                auth_info_1=username,
                auth_info_2=email,
                password=password
            )
            print(f"{datetime.now()} - Salvando cookies...")
            client.save_cookies(COOKIES)
            if os.path.exists(COOKIES):
                print(f"{datetime.now()} - Cookies salvos com sucesso em {COOKIES}.")
            else:
                print(f"{datetime.now()} - Erro: Os cookies não foram salvos.")

    except TwitterException as e:
        print("Falha ao efetuar login:", e)
    except Exception as e:
        print("Erro inesperado:", e)

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f"{datetime.now()} - Limite de taxa atingido. Aguardando até {rate_limit_reset} para continuar.")
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            time.sleep(wait_time)
            continue

        if not tweets:
            print(f"{datetime.now()} - Nenhum tweet encontrado.")
            break

        for tweet in tweets:
            tweet_count += 1
            searching_terms = {term for term in SEARCH_TERMS if term in tweet.text.lower()}
            search_term = ', '.join(sorted(searching_terms)) if searching_terms else 'Nenhum'

            tweet_data = [
                tweet_count,
                tweet.user.name,
                tweet.text,
                tweet.created_at,
                tweet.retweet_count,
                tweet.favorite_count,
                search_term
            ]

            with open(output_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f"{datetime.now()} - {tweet_count} tweets encontrados até agora.")

    print(f"{datetime.now()} - {tweet_count} tweets encontrados.")
