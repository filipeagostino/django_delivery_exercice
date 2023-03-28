import requests
from colorama import Fore, init
init(autoreset=True)

def cepValidator(cep):
    url = 'https://cdn.apicep.com/file/apicep/'

    cep_formated = cep[:5]+'-'+cep[5:]
    print(Fore.YELLOW + f'CEP FORMATED: {cep_formated}')

    result = requests.get(f'{url}{cep_formated}.json')
    
    if result.status_code == 200:
        print(Fore.GREEN + f'Status Code: {result.status_code}')
        result_json = result.json()
        print(f'Json:\n{result_json}')
        return True, result_json
    
    print(Fore.RED + 'Invalid CEP!')
    result_json = {}
    return False, result_json