import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_books import scrape_books


def scrape():
    """Scrape everything and return a list of books."""
    return  scrape_books(scrape_all_pages())


def write_books_to_csv(books, path):
    keys = books[0].keys()
    with open(path, 'w') as output:
        dict_writer = csv.DictWriter(output, delimiter=',', fieldnames = keys)
        dict_writer.writeheader()
        for row in books:
            dict_writer.writerow(row)    

def write_books_to_jsonl(data, output_path, append=False):
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
    return 
BASE_DIR = "artifacts"
CSV_PATH = os.path.join(BASE_DIR, "results.csv")
JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")
books = scrape()
write_books_to_csv(books,  CSV_PATH)
write_books_to_jsonl(books, JSONL_PATH)
    
if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")

    os.makedirs(BASE_DIR, exist_ok=True)

    book_urls = scrape_all_pages()
    books = scrape_books(book_urls)

    write_books_to_csv(books, CSV_PATH)
    write_books_to_jsonl(books, JSONL_PATH)

