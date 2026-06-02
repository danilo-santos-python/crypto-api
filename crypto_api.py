import requests
import logging

logging.basicConfig(level=logging.ERROR)

URL = "https://api.coingecko.com/api/v3/simple/price"

IDS = [
    "ripple",
    "stellar",
    "hedera-hashgraph",
    "ondo-finance",
    "xdce-crowd-sale",
    "kaspa"
]


def get_crypto_data():

    params = {
        "ids": ",".join(IDS),
        "vs_currencies": "usd,brl",
    }

    headers = {
        "User-Agent": "AquaaCryptoView/1.0"
    }

    try:

        response = requests.get(
            URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:

        logging.error(f"Erro API CoinGecko: {e}")

        return {}
