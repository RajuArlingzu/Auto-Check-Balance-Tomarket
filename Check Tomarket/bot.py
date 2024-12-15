import requests
import json
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Fungsi untuk mendapatkan token otentikasi
def get_auth_token(init_data):
    login_url = 'https://api-web.tomarket.ai/tomarket-game/v1/user/login'
    login_data = {
        "init_data": init_data,
        "invite_code": "",
        "from": "",
        "is_bot": False
    }
    try:
        response = requests.post(login_url, headers=headers, json=login_data)
        response.raise_for_status()  # Periksa jika ada kesalahan HTTP
        response_data = response.json()

        # Ambil token dan nama pertama
        access_token = response_data.get('data', {}).get('access_token')
        first_name = response_data.get('data', {}).get('fn', 'N/A')
        return access_token, first_name
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching auth token: {e}")
        return None, None
    except KeyError:
        print(Fore.RED + "Unexpected response structure when fetching auth token.")
        return None, None

# Header HTTP yang digunakan
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://mini-app.tomarket.ai',
    'priority': 'u=1, i',
    'referer': 'https://mini-app.tomarket.ai/',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99", "Microsoft Edge WebView2";v="130"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

token_check_url = 'https://api-web.tomarket.ai/tomarket-game/v1/token/balance'

# Baca file query
with open('query.txt', 'r') as file:
    queries = file.readlines()

total_total = 0  # Inisialisasi total

# Proses setiap query
for query in queries:
    init_data = query.strip()
    auth_token, first_name = get_auth_token(init_data)
    if not auth_token:
        print(Fore.RED + "Skipping due to auth token retrieval failure.")
        continue

    # Set header otorisasi
    headers['authorization'] = f'{auth_token}'

    data = {
        "language_code": "en",
        "init_data": init_data,
        "round": "One"  
    }

    try:
        response = requests.post(token_check_url, headers=headers, json=data)
        response.raise_for_status()  # Periksa jika ada kesalahan HTTP
        response_data = response.json()

        # Periksa format data
        data_fields = response_data.get('data', {})
        toma = data_fields.get('total', 0)  # Default ke 0 jika tidak ditemukan

        # Ambil jumlah (pastikan float konversi aman)
        try:
            amount = float(toma)  
        except (ValueError, TypeError):
            amount = 0

        total_total += amount

        # Tampilkan hasil untuk setiap akun
        print(Fore.MAGENTA + "Name:" + Style.RESET_ALL, first_name)
        print(Fore.GREEN + "Total:" + Style.RESET_ALL, amount)
        print('-' * 40)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error with {token_check_url}: {e}")
    except (json.JSONDecodeError, ValueError):
        print(Fore.RED + "Failed to parse JSON response or invalid amount.")

# Tampilkan total akhir
print(Fore.MAGENTA + f"Total Toma for all accounts: {total_total:.6f}")
