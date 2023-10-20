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
    main_url = f"https://www.walmart.com/search?q="
    for i in range(len(search)):
        main_url += search[i] + '+'
    
    # Helps bypass bot detection
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    
    print('Searching for products, please wait...')
    logging.info('Searching for products.')
    getProducts(main_url, HEADERS)

# For moving to the next pages to extract data
# <ul class="list flex items-center justify-center pa0"><li aria-hidden="false"><a link-identifier="Generic Name" class="sans-serif ph1 pv2 w4 h4 border-box bg-white br-100 b--solid ba mh2-m db tc no-underline b--light-gray" data-testid="PreviousPage" aria-label="Previous Page" href="/search?q=Monitor+&amp;page=24&amp;affinityOverride=default"><i class="ld ld-ChevronLeft pv1 primary" style="font-size: 1.5rem; vertical-align: -0.25em; width: 1.5rem; height: 1.5rem; box-sizing: content-box;"></i></a></li><li><a link-identifier="Generic Name" class="sans-serif ph1 pv2 w4 h4 lh-copy border-box br-100 b--solid mh2-m db tc no-underline black bg-white b--white-90" aria-label="Go to Page 1" data-automation-id="page-number" href="/search?q=Monitor+&amp;affinityOverride=default">1</a></li><li><div class="sans-serif pa1 lh-copy border-box bg-white">...</div></li><li><a link-identifier="Generic Name" class="sans-serif ph1 pv2 w4 h4 lh-copy border-box br-100 b--solid mh2-m db tc no-underline black bg-white b--white-90" aria-label="Go to Page 22" data-automation-id="page-number" href="/search?q=Monitor+&amp;page=22&amp;affinityOverride=default">22</a></li><li><a link-identifier="Generic Name" class="sans-serif ph1 pv2 w4 h4 lh-copy border-box br-100 b--solid mh2-m db tc no-underline black bg-white b--white-90" aria-label="Go to Page 23" data-automation-id="page-number" href="/search?q=Monitor+&amp;page=23&amp;affinityOverride=default">23</a></li><li><a link-identifier="Generic Name" class="sans-serif ph1 pv2 w4 h4 lh-copy border-box br-100 b--solid mh2-m db tc no-underline black bg-white b--white-90" data-automation-id="page-number" href="/search?q=Monitor+&amp;page=24&amp;affinityOverride=default" aria-label="Go to Page 24">24</a></li><li><div class="sans-serif ph1 pv2 w4 h4 lh-copy border-box br-100 b--solid mh2-m db tc no-underline gray bg-white b b--primary">25</div></li></ul>
# https://www.walmart.com/search?q=Monitor+&page=2&affinityOverride=default


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