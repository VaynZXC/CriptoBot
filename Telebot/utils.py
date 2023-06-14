import requests
import json
from config import keys


class ConversionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionExeption('Укажите разные валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionExeption(f'Не удалось обрабовать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionExeption(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionExeption(f'Введите верное число.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base