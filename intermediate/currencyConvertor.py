from bs4 import BeautifulSoup
import requests

'''
This is just a CLI based app, GUI to be added soon.
You would need an open exchange rates account for an app_id
'''

def convert_currency(baseCurrency, amount, currency2):
    pass

def availableCurrencies():
    url = "https://docs.openexchangerates.org/reference/supported-currencies"
    page = requests.get(url).text

    soup = BeautifulSoup(page, 'lxml')
    table = soup.find('table') # Get the first table from the webpage
    
    # Extract table headings
    headings = [th.text.strip() for th in table.find_all('th')]

    # Extract table rows and data
    row_data = [[td.text.strip() for td in row.find_all('td')] for row in table.find_all('tr')]

    # Print the table headers and data
    print('\t'.join(headings))
    
    for row in row_data:
        print('\t'.join(row))
    print() # Newline

def getCurrencies():
    return
    app_id = "Your_App_Id"
    
    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
    response = requests.get(url)
    data = response.json()
    print(data)

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
    # currencies = getCurrencies()
    while True:
        try:
            options()
            response = int(input('> '))
            if response == 1:
                print('Please wait, fetching available currencies...\n')
                availableCurrencies()
            elif response == 2:
                baseCurrency = input("Enter a base currency: ").upper()
                amount = float(input(f"Enter amount in {baseCurrency}: "))
                currency2 = input("Enter a currency to convert to: ").upper()
                result = convert_currency(baseCurrency, amount, currency2)
                print(f"{amount} {baseCurrency} in {currency2} is {result}")
            elif response == 3:
                pass
            elif response == 4:
                print("Quitting..")
                break
            else:
                print("Invalid option.")
        except ValueError:
            print("Invalid!")


if __name__ == "__main__":
    try:
        banner()
        main()
    except KeyboardInterrupt:
        print("\nEnding script...")