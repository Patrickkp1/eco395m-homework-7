from common import get_soup

def extract_price(price_str):
    if 'Â' in price_str:
        price_str = price_str.split('Â')[1]
    """Extracts the price form the string in the product description as a float."""
    return float(price_str[1:])


def extract_stock(stock_str):
    """Extracts the count form the string in the product description as an int."""

    return int(stock_str.split()[2][1:])

def get_category(soup):
    """Extracts the category from the BeautifulSoup instance representing a book page as a string."""

    line = soup.find('ul', {'class':'breadcrumb'}).text.split('\n')
    return [e for e in line if e][2]


def get_title(soup):
    """Extracts the title from the BeautifulSoup instance representing a book page as a string."""
    
    return soup.find('h1').text


def get_description(soup):
    """Extracts the description from the BeautifulSoup instance representing a book page as a string."""
    if '\n' in soup.find_all('p')[3].text:
        return None
    return soup.find_all('p')[3].text


def get_product_information(soup):
    """Extracts the product information from the BeautifulSoup instance representing a book page as a dict."""
    d = {}
    for tr in soup.find_all('table'):
        line = (tr.get_text(separator = '|').split('|'))
        if len(line) > 1:  
            line = [e.replace('\n', '') for e in line]
            line = [e for e in line if e != '']
            for i in range(len(line)):
                if (line[i][:2]) == 'Â£':
                    line[i] = extract_price(line[i])
                elif 'stock' in line[i].split(): 
                    line[i] = extract_stock(line[i])
                else: 
                    pass
            for key, val in list(zip(line[0::2], line[1::2])):
                    d[key] = val
    new_d = {k: v for k, v in d.items() if k.lower() == 'upc' or k.lower() == 'price (excl. tax)' or
             k.lower() == 'availability' }
    new_d['upc'] = new_d.pop('UPC')
    new_d['price_gbp'] = new_d.pop('Price (excl. tax)')
    new_d['stock'] = new_d.pop('Availability')

    return new_d

def scrape_book(book_url):
    soup = get_soup(book_url)
    
    d = get_product_information(soup)
    """Extracts all information from a book page and returns a dict."""
    d['title'] = get_title(soup)
    d['category'] = get_category(soup)
    d['description'] = get_description(soup)
    
    sorted_d = {}
    for key in ['upc', 'title', 'category', 'description', 'price_gbp', 'stock']: 
        sorted_d[key] = d[key]
    return sorted_d


def scrape_books(book_urls):
    list_of_dicts = []
    for link in book_urls: 
        list_of_dicts.append(scrape_book(link))        
    """Extracts all information from a list of book page and returns a list of dicts."""
    return list_of_dicts


if __name__ == "__main__":

    # code for testing

    # set up fixtures for testing

    book_url = "http://books.toscrape.com/catalogue/the-secret-of-dreadwillow-carse_944/index.html"
    book_url_no_description = "http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html"

    soup = get_soup(book_url)
    soup_no_description = get_soup(book_url_no_description)

    # test extract_price

    assert extract_price("£56.13") == 56.13

    # test extract_stock

    assert extract_stock("In stock (16 available)") == 16

    # test get_category

    assert get_category(soup) == "Childrens"

    # test get_title

    assert get_title(soup) == "The Secret of Dreadwillow Carse"

    # test get_description

    assert get_description(soup) is not None
    assert get_description(soup_no_description) is None

    # test get_product_information

    product_information = get_product_information(soup)

    assert set(product_information.keys()) == {"upc", "price_gbp", "stock"}

    assert product_information == {
        "upc": "b5ea0b5dabed25a8",
        "price_gbp": 56.13,
        "stock": 16,
    }

    # test scrape_book

    book = scrape_book(book_url)
    book_no_description = scrape_book(book_url_no_description)

    expected_keys = {"title", "category", "description", "upc", "price_gbp", "stock"}

    assert set(book.keys()) == expected_keys
    assert set(book_no_description.keys()) == expected_keys
