import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_books import scrape_books


def scrape():
    """Scrape everything and return a list of books."""
    return None


def write_books_to_csv(books, path):
    pass


def write_books_to_jsonl(books, path):
    pass


if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")

    os.makedirs(BASE_DIR, exist_ok=True)

    book_urls = scrape_all_pages()
    books = scrape_books(book_urls)

    write_books_to_csv(books, CSV_PATH)
    write_books_to_jsonl(books, JSONL_PATH)
