import sys
import argparse
from utils import Scraper, save_dataframe_to_csv, analyze_frequency
from count import count_words_for_phrase

BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

class WikiController:
    """
    Controller class that manages the program flow.
    It takes parsed arguments and coordinates calls to other modules.
    """
    def __init__(self, args):
        self.args = args

    def run(self):
        if self.args.analyze_relative_word_frequency:
            if not self.args.mode or not self.args.count:
                print("Error: --mode and --count are required when using --analyze-relative-word-frequency")
                sys.exit(1)
            from word_frequency import analyze_relative_frequency
            analyze_relative_frequency(self.args.mode, self.args.count, self.args.chart)
            return

        if self.args.auto_count_words:
            from auto_count import auto_count_bfs
            auto_count_bfs(BULBAPEDIA_URL, self.args.auto_count_words, self.args.depth, self.args.wait)
            return

        if self.args.count_words:
            count_words_for_phrase(BULBAPEDIA_URL, self.args.count_words)
            return
        
        scraper = Scraper(BULBAPEDIA_URL, self.args.summary or self.args.table)
        
        if self.args.summary:
            print(scraper.get_summary())
            
        if self.args.table:
            if not self.args.number:
                print("Error: --number argument is required when using --table.")
                sys.exit(1)
            
            df = scraper.get_table(self.args.number, self.args.first_row_is_header)
            if df is not None:
                save_dataframe_to_csv(df, self.args.table)
                analyze_frequency(df, self.args.table)

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
    parser.add_argument("--analyze-relative-word-frequency", action="store_true", help="Analyze relative word frequency compared to language")
    parser.add_argument("--mode", choices=["article", "language"], help="Sorting mode for frequency analysis")
    parser.add_argument("--count", type=int, help="Number of rows/bars to display")
    parser.add_argument("--chart", help="Path to save the frequency chart")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    app = WikiController(args)
    app.run()

if __name__ == "__main__":
    main()
