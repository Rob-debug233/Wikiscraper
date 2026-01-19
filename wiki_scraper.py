import sys
import argparse
import requests
from bs4 import BeautifulSoup

BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

def get_summary(phrase):
    url = f"{BULBAPEDIA_URL}{phrase.replace(' ', '_')}"
    
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return f"Error: Article for '{phrase}' not found on Bulbapedia."
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Minimalist approach: find the first non-empty <p> tag
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if text:
            return text
    
    return "Error: Could not find any summary paragraph for this article."

def main():
    parser = argparse.ArgumentParser(description="Wiki Scraper Tool")
    parser.add_argument("--summary", help="Fetch a short summary for the given phrase")
    
    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.summary:
        result = get_summary(args.summary)
        print(result)

if __name__ == "__main__":
    main()
