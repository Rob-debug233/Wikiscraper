import sys
import argparse
from utils import Scraper, save_dataframe_to_csv, analyze_frequency
from count import count_words_for_phrase

BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

def main():
    parser = argparse.ArgumentParser(description="Wiki Scraper Tool")
    parser.add_argument("--summary", help="Fetch a short summary for the given phrase")
    parser.add_argument("--table", help="Fetch a table for the given phrase")
    parser.add_argument("--number", type=int, help="The number of the table to extract (1-based)")
    parser.add_argument("--first-row-is-header", action="store_true", help="Treat the first row as the header")
    parser.add_argument("--count-words", help="Count words in the article and save to word-counts.json")
    parser.add_argument("--auto-count-words", help="BFS crawl starting from this phrase and count words")
    parser.add_argument("--depth", type=int, default=1, help="Maximum depth for BFS crawl")
    parser.add_argument("--wait", type=float, default=0.1, help="Wait time between requests in seconds")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.auto_count_words:
        from auto_count import auto_count_bfs
        auto_count_bfs(BULBAPEDIA_URL, args.auto_count_words, args.depth, args.wait)
        return

    if args.count_words:
        count_words_for_phrase(BULBAPEDIA_URL, args.count_words)
        return
    
    # Stwórz scraper
    scraper = Scraper(BULBAPEDIA_URL, args.summary or args.table)
    
    if args.summary:
        result = scraper.get_summary()
        print(result)
        
    if args.table:
        if not args.number:
            print("Error: --number argument is required when using --table.")
            sys.exit(1)
        
        # Pobierz tabelę
        df = scraper.get_table(args.number, args.first_row_is_header)
        if df is not None:
            # Zapisz do CSV
            save_dataframe_to_csv(df, args.table)
            # Wyświetl analizę
            analyze_frequency(df, args.table)

if __name__ == "__main__":
    main()
