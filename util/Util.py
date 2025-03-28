import requests
import re

def get_ceps(addresses, google_maps_api_key, logger):
    if not addresses:
        logger.error("Endereços não fornecidos para a API do Google Maps.")
        return []

    ceps = []
    for address in addresses:
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
                        ceps.append(component['long_name'])
                        break
                else:
                    logger.warning(f"CEP não encontrado para o endereço: {address}")
            else:
                logger.warning(f"Endereço não encontrado: {address}")
        else:
            logger.error(f"Erro na API: {response.status_code}, {response.text}")

    return ceps

def get_coordinates(ceps, addresses, google_maps_api_key, logger):
    if not ceps and not addresses:
        logger.error("CEPs e endereços não fornecidos para a API do Google Maps.")
        return [], []

    latitudes = []
    longitudes = []

    queries = ceps if ceps else addresses
    if not ceps:
        logger.info("CEPs não fornecidos, utilizando endereços para buscar coordenadas.")
        queries = [address + ", Bauru, São Paulo, Brasil" if "Bauru" not in address else address for address in addresses]

    for query in queries:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {'address': query, 'key': google_maps_api_key}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                location = data['results'][0]['geometry']['location']
                latitudes.append(location['lat'])
                longitudes.append(location['lng'])
            else:
                logger.warning(f"Localização não encontrada para: {query}")
                latitudes.append(None)
                longitudes.append(None)
        else:
            logger.error(f"Erro na API: {response.status_code}, {response.text}")
            latitudes.append(None)
            longitudes.append(None)

    return latitudes, longitudes

def extract_addresses(content, logger):
    address_pattern = r"(Rua|Bairro|Acampamento|Avenida|Praça|Travessa|Alameda|Vila|Jardim|Parque|Residencial|Conjunto Habitacional|Rodovia|Núcleo)\s+([A-Za-zÀ-ÖØ-öø-ÿ\s]+)(?=,|\.|$)"
    matches = re.findall(address_pattern, content, re.IGNORECASE)

    unique_addresses = set()  # Conjunto para evitar repetições
    address_types = set()

    for match in matches:
        address_type = match[0]
        address_name = match[1]
        full_address = f"{address_type} {address_name}".strip()

        # Normaliza removendo caracteres especiais e espaços desnecessários
        full_address = re.sub(r"[^\w\s,]", "", full_address)

        if full_address not in unique_addresses:
            unique_addresses.add(full_address)
            address_types.add(address_type)
            logger.info(f"Endereço extraído: {full_address}")

    if not unique_addresses:
        logger.warning("Nenhum endereço encontrado no conteúdo.")

    return list(unique_addresses), list(address_types)

def remove_semicolons(text):
    return text.replace(';', '')

# Remove espaços duplicados, rodando o texto 3 vezes para garantir que todos os espaços extras sejam removidos
def remove_duplicate_spaces(text):
    for _ in range(3):
        text = ' '.join(text.split())
    return text.strip()
