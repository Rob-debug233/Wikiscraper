import os
import sys
from utils import Scraper

TEST_DIR = "test"
BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

def test_summary_offline():
    """Test get_summary z lokalnego pliku HTML - logic form test_scraper.py"""
    print("Running integration test: test_summary_offline...")
    html_file = os.path.join(TEST_DIR, "Lugia.html")
    
    if not os.path.exists(html_file):
        print(f"Error: Test file '{html_file}' not found.")
        sys.exit(1)

    scraper = Scraper(
        base_url=BULBAPEDIA_URL,
        phrase="Lugia",
        use_local_html_file=True,
        html_file_path=html_file
    )
    
    result = scraper.get_summary()
    expected = "Lugia (Japanese: ルギア Lugia) is a dual-type Psychic/Flying Legendary Pokémon introduced in Generation II."
    
    if result == expected:
        print("SUCCESS")
        sys.exit(0)
    else:
        print("FAILURE")
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        sys.exit(1)

if __name__ == "__main__":
    test_summary_offline()
