import requests
import re

def get_cep(address, google_maps_api_key, logger):
    if not address:
        logger.error("Endereço não fornecido para a API do Google Maps.")
        return None

    if "Bauru" not in address:
        address += ", Bauru, São Paulo, Brasil"

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': google_maps_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            address_components = data['results'][0]['address_components']
            for component in address_components:
                if 'postal_code' in component['types']:
                    return component['long_name']
            logger.warning(f"CEP não encontrado para o endereço: {address}")
            return None
        else:
            logger.warning(f"Endereço não encontrado: {address}")
            return None
    else:
        logger.error(f"Erro na API: {response.status_code}, {response.text}")
        return None

def get_coordinates(cep, address, google_maps_api_key, logger):
    if not cep and not address:
        logger.error("CEP e endereço não fornecido para a API do Google Maps.")
        return None, None

    if not cep:
        logger.info("CEP não fornecido, utilizando endereço para buscar coordenadas.")
        query = address

        if "Bauru" not in query:
            query += ", Bauru, São Paulo, Brasil"
    else:
        query = cep

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': query, 'key': google_maps_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logger.warning(f"Localização não encontrada para: {query}")
            return None, None
    else:
        logger.error(f"Erro na API: {response.status_code}, {response.text}")
        return None, None

def extract_address(content, logger):
    # Expressão regular para encontrar endereços e tipos de endereço
    address_pattern = r"(Rua|Bairro|Acampamento|Avenida|Praça|Travessa|Alameda|Vila|Jardim|Parque|Residencial|Conjunto Habitacional|Rodovia|Núcleo)\s+[A-Za-zÀ-ÖØ-öø-ÿ\s]+(?=,|\.|$)"
    match = re.search(address_pattern, content, re.IGNORECASE)

    if match:
        address = match.group(0)
        address_type = match.group(1)  # Captura o tipo de endereço
        address = re.sub(r"[^\w\s,]", "", address)  # Remove caracteres especiais
        address = address.strip()  # Remove espaços em branco no início e no final
        logger.info(f"Endereço extraído: {address}")
        return address, address_type
    else:
        logger.warning("Nenhum endereço encontrado no conteúdo.")
        return None, None

def remove_semicolons(text):
    return text.replace(';', '')

# Remove espaços duplicados, rodando o texto 3 vezes para garantir que todos os espaços extras sejam removidos
def remove_duplicate_spaces(text):
    for _ in range(3):
        text = ' '.join(text.split())
    return text.strip()
