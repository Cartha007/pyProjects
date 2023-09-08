from bs4 import BeautifulSoup
import requests

'''
This is just a CLI based app, GUI to be added soon.
You would need an open exchange rates account for an app_id
'''

def availableCurrencies():
    url = "https://docs.openexchangerates.org/reference/supported-currencies"
    page = requests.get(url).text

    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table') # Get the first table from the webpage
    
    # Extract table headings
    headings = [th.text.strip() for th in table.find_all('th')]

    # Extract table rows and data
    row_data = [[td.text.strip() for td in row.find_all('td')] for row in table.find_all('tr')]
    
    return headings, row_data

def listCurrencies():
    data = availableCurrencies()
    # Print the table headers and data
    headings, row_data = availableCurrencies()
    
    print('\t'.join(headings))
    
    for row in row_data:
        print('\t'.join(row))
    print() # Newline

def isCurrencyAvailable(baseCurrency):
    _, currencies = availableCurrencies()
    return baseCurrency in [x[0] for x in currencies if x]

def getCurrencyName(currency):
    _, currencies = availableCurrencies()
    name = [x[1] for x in currencies if x and x[0] == currency][0]
    return name if name else "Unknown name"

def getCurrency(currency):
    app_id = "Your_App_Id"
    
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&symbols={currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'][currency]

def format_currency(value: (float, int), place: int =2):
    #Round to two decimal places and ensure a trailing zero
    return f'{round(value, place):.{place}f}'

def convert_currency(baseCurrency, amount, currency2):
    if baseCurrency == currency2:
        return amount
    if baseCurrency == "USD":
        usdTocurrency = getCurrency(currency2)
        result = usdTocurrency * amount
    elif currency2 == "USD":
        currency2ToUSD = getCurrency(baseCurrency)
        result = amount / currency2ToUSD
    else:
        baseCurrencyToUSD = getCurrency(baseCurrency)
        currency2ToUSD = getCurrency(currency2)
        result = (amount / baseCurrencyToUSD) * currency2ToUSD
    return format_currency(result)

def convert_currency_prompt():
    baseCurrency = input("Enter a base currency: ").upper()
    if isCurrencyAvailable(baseCurrency):
        amount = float(input(f"Enter amount in {baseCurrency}: "))
        currency2 = input("Enter a currency to convert to: ").upper()
        if isCurrencyAvailable(currency2):
            name = getCurrencyName(currency2)
            result = convert_currency(baseCurrency, amount, currency2)
            print(f"{format_currency(amount)} {baseCurrency} in {currency2}({name}) is {result}")
        else:
            print("Currency not available.")
    else:
        print("Currency not available.")
        
def getExchangeRate(currency1, currency2):
    if currency1 == currency2:
        rate = "1.00"
    usdToCurrency1 = getCurrency(currency1)
    usdToCurrency2 = getCurrency(currency2)
    rate = usdToCurrency2 / usdToCurrency1
    rate = format_currency(rate, 3)
    print(f'Exchange rate for 1 {currency1} in {currency2} is {rate}')

def getExchangeRate_prompt():
    currency1 = input("Enter currency 1: ").upper()
    if isCurrencyAvailable(currency1):
        currency2 = input("Enter currency 2: ").upper()
        if isCurrencyAvailable(currency2):
            getExchangeRate(currency1, currency2)
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
    while True:
        try:
            options()
            response = int(input('> '))
            if response == 1:
                print('Please wait, fetching available currencies...\n')
                listCurrencies()
            elif response == 2:
                convert_currency_prompt()
            elif response == 3:
                getExchangeRate_prompt()
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
    main()
