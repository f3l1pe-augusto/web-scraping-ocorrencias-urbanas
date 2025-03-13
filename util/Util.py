import requests
import re

def get_coordinates(address, google_maps_api_key, logger):
    if not address:
        logger.error("Endereço não fornecido para a API do Google Maps.")
        return None, None

    if "Bauru" not in address:
        address += ", Bauru, São Paulo, Brasil"

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {'address': address, 'key': google_maps_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            logger.warning(f"Endereço não encontrado: {address}")
            return None, None
    else:
        logger.error(f"Erro na API: {response.status_code}, {response.text}")
        return None, None

def extract_address(content, logger):
    # Expressão regular para encontrar endereços e tipos de endereço
    address_pattern = r"(Rua|Bairro|Acampamento|Avenida|Praça|Travessa|Alameda|Vila|Jardim|Parque|Residencial|Conjunto Habitacional|Rodovia|Núcleo|Hospital)\s+[A-Za-zÀ-ÖØ-öø-ÿ\s]+(?=,|\.|$)"
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
