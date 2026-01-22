import json
import re
import os
from collections import Counter
from utils import Scraper

WORD_COUNTS_FILE = "word-counts.json"

def count_words_from_html(soup):
    """
    Zlicza słowa w tekście artykułu z BeautifulSoup obiektu.
    Używa standardowego ID 'mw-content-text' (Wikipedii/Bulbapedii).
    """
    if not soup:
        return Counter()
    
    # Znajdź główny kontener tekstu artykułu
    article_content = soup.find('div', id='mw-content-text')
    
    if not article_content:
        return Counter()

    # Usuń elementy, które psują statystyki
    for element in article_content(['script', 'style', 'table', 'noscript']):
        element.decompose()

    # Pobierz czysty tekst
    text = article_content.get_text(separator=' ')
    
    # Oczyść i podziel na słowa (małe litery)
    words = re.findall(r'\b\w+\b', text.lower())
    
    return Counter(words)

def update_word_counts(new_counts):
    """
    Load, update, and save word counts.
    """
    counts = Counter()
    if os.path.exists(WORD_COUNTS_FILE):
        with open(WORD_COUNTS_FILE, 'r', encoding='utf-8') as f:
            counts.update(json.load(f))
    
    counts.update(new_counts)
    
    with open(WORD_COUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(dict(counts), f, indent=4, ensure_ascii=False)

def count_words_for_phrase(base_url, phrase, use_local_html_file=False, html_file_path=None):
    """
    Główna funkcja: pobiera stronę, liczy słowa i aktualizuje word-counts.json
    """
    scraper = Scraper(
        base_url=base_url,
        phrase=phrase,
        use_local_html_file=use_local_html_file,
        html_file_path=html_file_path
    )
    
    if not scraper.soup:
        print(f"Error: Could not load page for '{phrase}'")
        return
    
    # Policz słowa
    word_counter = count_words_from_html(scraper.soup)
    
    if not word_counter:
        print(f"Error: No words found in article '{phrase}'")
        return
    
    # Aktualizuj JSON
    update_word_counts(word_counter)
