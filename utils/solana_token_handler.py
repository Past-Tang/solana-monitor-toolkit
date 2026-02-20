import requests


def fetch_data(tokencode):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(
            f'https://gmgn.ai/defi/quotation/v1/trades/sol/{tokencode}?limit=100&maker=&tag[]=smart_degen&tag[]=pump_smart',
            headers=headers,
        )
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if 'data' in data and 'history' in data['data']:
            smarlen = [i["maker"] for i in data['data']['history']]
            return len(list(set(smarlen)))
        else:
            return 0
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except KeyError as key_err:
        print(f"Key error: {key_err}")
    except ValueError as val_err:
        print(f"JSON decoding failed: {val_err}")
    return 0

if __name__ == '__main__':
    result = fetch_data('5V19hKvVAXCqpS7m6oVTZXHQEhmVefu4kUFJHEiBpump')
    print(result)