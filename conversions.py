import requests

URL = "https://api.getgeoapi.com/v2/currency"
API_KEY = "ffed1e290ade59232d49ba9f3f86da0c97a00df6"


def get_currencies_list():
    currencies_list_url = URL + "/list"
    params = {
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(currencies_list_url, params=params)

    if response.status_code == 200:
        data = response.json()
        sorted_currencies = sorted(data["currencies"].items(), key=lambda item: str(item[0]))
        return [f"{k} - {v}" for k, v in sorted_currencies]
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def convert(base_currency: str, target_currency: str, amount: float):
    convert_url = URL + "/convert"
    params = {
        "api_key": API_KEY,
        "from": base_currency,
        "to": target_currency,
        "amount": amount,
        "format": "json"
    }

    response = requests.get(convert_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data  # Return the conversion data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
