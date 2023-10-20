from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(filename='walmartscraper.log', level=logging.DEBUG, 
                    format='%(asctime)s- %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def getProductInfo(url, HEADERS):
    # Send an HTTP GET request
    # logging.info('Sending an HTTP GET request.')
    response = requests.get(url, headers=HEADERS)
    logging.info(f'Status: {response.status_code}')
    if response.status_code == 200:
        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'lxml')
        logging.info('Parsed the webpage content with BeautifulSoup.')
        
        # Extract the product title
        product_title = soup.find('h1', {'id': 'main-title'}).text.strip() if soup.find('h1', {'id': 'main-title'}) else None
        if product_title:
            logging.info(f'Get product info for: {product_title}')
        print('Product Title:', product_title)

        # Extract rating number
        rating_number = soup.find('span', {'class': 'f7 rating-number'}).text.strip() if soup.find('span', {'class': 'f7 rating-number'}) else None
        print('Rating Number:', rating_number)

        # Extract review count
        review_count = soup.find('a', {'itemprop': 'ratingCount'}).text.strip() if soup.find('a', {'itemprop': 'ratingCount'}) else None
        print('Review Count:', review_count)
        
        # Extract price
        price = soup.find('span', {'itemprop': 'price'}).text.strip() if soup.find('span', {'itemprop': 'price'}) else None
        print('Price:', price)
        logging.info('Extracted info.')
    else:
        print('Failed to retrieve the page. Status code:', response.status_code)
        logging.error(f'Failed to retrieve the page. Status code: {response.status_code}')


def getProducts(url, HEADERS):
    # Send an HTTP GET request
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logging.info(f'Status: {response.status_code}')
        soup = BeautifulSoup(response.text, 'lxml')
    
        # Fetch links to individual product pages
        product_links = soup.find_all('a', attrs={'class': 'absolute w-100 h-100 z-1 hide-sibling-opacity'})
        
        for link in product_links:
            product_url = link.get("href")
            if product_url.startswith('/'):
                product_url = 'https://www.walmart.com' + product_url
            # print(f'Visiting Product URL: {product_url}')
            # logging.info(f'Visiting Product URL: {product_url}')
            getProductInfo(product_url, HEADERS)
    
def main():
    print('''====== Cartha's Walmart Scraper ======\n''')
    print('Enter your keyword to search for')
    search = input('>').split(" ")
    logging.info(f'Entered keyword: {search}')
    main_url = f"https://www.walmart.com/search?q={search}"
    for i in range(len(search)):
        main_url += search[i] + '+'
    
    # Helps bypass bot detection
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    
    print('Searching for products, please wait...')
    logging.info('Searching for products.')
    getProducts(main_url, HEADERS)


if __name__ == '__main__':
    print('Starting script...')
    logging.info('Started script.')
    # check_internet_connection()
    try:
        main()
    except KeyboardInterrupt:
        pass
    # except Exception as e:
    #     print(e)
    finally:
        logging.info('Script ended.')
        print('Script ended.')