from bs4 import BeautifulSoup
import requests

def getProductInfo(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    # Send an HTTP GET request
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract product title
        product_title = soup.find('h1', {'id': 'main-title'}).text.strip()
        print('Product Title:', product_title)

        # Extract rating number
        rating_number = soup.find('span', {'class': 'f7 rating-number'}).text.strip()
        print('Rating Number:', rating_number)

        # Extract review count
        review_count = soup.find('a', {'itemprop': 'ratingCount'}).text.strip()
        print('Review Count:', review_count)

        # Extract price
        price = soup.find('span', {'itemprop': 'price'}).text.strip()
        print('Price:', price)
    else:
        print('Failed to retrieve the page. Status code:', response.status_code)

def getProducts(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # Fetch links to individual product pages
        product_links = soup.find_all('a', {'class': 'absolute w-100 h-100 z-1 hide-sibling-opacity'})
        
        for link in product_links:
            product_url = link.get('href')
            if product_url.startswith('/'):
                product_url = 'https://www.walmart.com' + product_url
            print('Visiting Product URL:', product_url)
            getProductInfo(product_url)

def main():
    print('''====== Walmart Scraper ======\n''')

    main_url = "https://www.walmart.com/search?q=Monitor"
    print('Searching for products, please wait...')
    getProducts(main_url)

if __name__ == '__main__':
    print('Starting script...')
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('Script ended.')
