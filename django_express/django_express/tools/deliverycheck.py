import requests
from colorama import Fore, init
init(autoreset=True)


def getInfo(originzipCode, destzipCode, weight):
        
    url = f'https://www.cepcerto.com/ws/json-frete/{originzipCode}/{destzipCode}/{weight}'

    print(Fore.MAGENTA + f'URL: {url}')

    result = requests.get(url)

    if result.status_code == 200:
        print(Fore.GREEN + f'Status Code: {result.status_code}')
        result_json = result.json()
        print(f'Json:\n{result_json}')

        return result_json
