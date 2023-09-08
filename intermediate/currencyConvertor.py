from bs4 import BeautifulSoup
import requests, time

'''
This is just a CLI based app, GUI to be added soon.
You would need an open exchange rates account for an app_id
'''

def fetch_page():
    try:
        url = "https://docs.openexchangerates.org/reference/supported-currencies"
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def available_currencies():
    page = fetch_page()
    
    if page is None:
        return None

    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table')  # Get the first table from the webpage
    
    # Extract table headings
    headings = [th.text.strip() for th in table.find_all('th')]

    # Extract table rows and data
    row_data = [[td.text.strip() for td in row.find_all('td')] for row in table.find_all('tr')]
    
    return headings, row_data

def list_currencies(data):
    if data is None:
        return None
    
    # Print the table headers and data
    headings, row_data = data
    
    print('\t'.join(headings))
    
    for row in row_data:
        print('\t'.join(row))
    print()  # Newline

def is_currency_available(baseCurrency, data):
    if data is None:
        return False
    
    _, currencies = data
    return baseCurrency in [x[0] for x in currencies if x]

def get_currency_name(currency, data):
    if data is None:
        return "Unknown name"
    
    _, currencies = data
    name = [x[1] for x in currencies if x and x[0] == currency][0]
    return name if name else "Unknown name"

def get_currency(currency):
    try:
        app_id = "Your_App_Id"
        
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={currency}"
        response = requests.get(url)
        data = response.json()
        return data['rates'][currency]
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching currency data: {e}")
        return None

def format_currency(value: (float, int), place: int =2):
    #Round to two decimal places and ensure a trailing zero
    return f'{round(value, place):.{place}f}'

def convert_currency(baseCurrency, amount, currency2):
    if baseCurrency == currency2:
        return amount
    base_rate = get_currency(baseCurrency)
    target_rate = get_currency(currency2)
    
    if base_rate is None or target_rate is None:
        return None
    
    result = (amount / base_rate) * target_rate
    return format_currency(result)

def convert_currency_prompt(data):
    baseCurrency = input("Enter a base currency: ").upper()
    if is_currency_available(baseCurrency, data):
        amount = float(input(f"Enter amount in {baseCurrency}: "))
        currency2 = input("Enter a currency to convert to: ").upper()
        if is_currency_available(currency2, data):
            name = get_currency_name(currency2, data)
            result = convert_currency(baseCurrency, amount, currency2)
            if result is not None:
                print(f"{format_currency(amount)} {baseCurrency} in {currency2}({name}) is {result}")
            else:
                print("Error in currency conversion. Possible cause: No internet connection or invalid app_id")
        else:
            print("Currency not available.")
    else:
        print("Currency not available.")
        
def get_exchange_rate(currency1, currency2):
    if currency1 == currency2:
        rate = "1.00"
    usdToCurrency1 = get_currency(currency1)
    usdToCurrency2 = get_currency(currency2)
    
    if usdToCurrency1 is not None and usdToCurrency2 is not None:
        rate = usdToCurrency2 / usdToCurrency1
        rate = format_currency(rate, 3)
        print(f'Exchange rate for 1 {currency1} in {currency2} is {rate}')
    else:
        print("Error in fetching exchange rate.  Possible cause: No internet connection or invalid app_id")

def get_exchange_rate_prompt(data):
    currency1 = input("Enter currency 1: ").upper()
    if is_currency_available(currency1, data):
        currency2 = input("Enter currency 2: ").upper()
        if is_currency_available(currency2, data):
            get_exchange_rate(currency1, currency2)
        else:
            print("Currency not available.")
    else:
        print("Currency not available.")

def options():
    print("Select an option:")
    print("[1] List the available currencies")
    print("[2] Convert from one currency to another")
    print("[3] Get the exchange rate of two currencies")
    print("[4] Quit the program")

def banner():
    print("╔════════════════════════╗")
    print("║   \033[1;36mCurrency Converter\033[0m   ║")
    print("╚════════════════════════╝")

def main():
    banner()
    currencies_data = available_currencies()
    while True:
        try:
            options()
            response = int(input('> '))
            if response == 1:
                print('Please wait, fetching available currencies...\n')
                list_currencies(currencies_data)
            elif response == 2:
                convert_currency_prompt(currencies_data)
                time.sleep(3)
            elif response == 3:
                get_exchange_rate_prompt(currencies_data)
                time.sleep(3)
            elif response == 4:
                print("Quitting..")
                break
            else:
                print("Invalid option.")
        except KeyboardInterrupt:
            print("\nEnding script...")
            break
        except ValueError:
            print("Invalid input! Enter a valid option.")


if __name__ == "__main__":
    print("Starting, please wait...")
    main()
