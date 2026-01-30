import unittest
import os
import json
import pandas as pd
from utils import Scraper, string_to_windows_safe
from count import count_words_for_phrase, WORD_COUNTS_FILE

TEST_DIR = "test"
BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

class TestWikiScraper(unittest.TestCase):
    
    def test_word_counts_accumulation(self):
        """Test word counting and accumulation (1-1 from test_word_counts_accumulation)"""
        reference_file = os.path.join(TEST_DIR, "word-counts_Type_two_times.json")
        
        if os.path.exists(WORD_COUNTS_FILE):
            os.remove(WORD_COUNTS_FILE)
        
        try:
            # Count twice for "Type"
            count_words_for_phrase(BULBAPEDIA_URL, "Type")
            count_words_for_phrase(BULBAPEDIA_URL, "Type")
            
            with open(WORD_COUNTS_FILE, 'r', encoding='utf-8') as f:
                generated_data = json.load(f)
            with open(reference_file, 'r', encoding='utf-8') as f:
                reference_data = json.load(f)
                
            self.assertEqual(generated_data, reference_data, "Generated word stats differ!")
            
        finally:
            if os.path.exists(WORD_COUNTS_FILE):
                os.remove(WORD_COUNTS_FILE)

    def test_summary_not_found(self):
        """Test get_summary for non-existent article (1-1 from test_summary_not_found)"""
        scraper = Scraper(
            base_url=BULBAPEDIA_URL,
            phrase="adgadadagdasg"
        )
        
        result = scraper.get_summary()
        self.assertEqual(result, "Error: Could not load page.")

    def test_tao_trio_without_header(self):
        """Test Tao trio WITHOUT --first-row-is-header (1-1 from test_tao_trio_without_header)"""
        html_file = os.path.join(TEST_DIR, "Tao trio.html")
        expected_file = os.path.join(TEST_DIR, "Tao trio without flag.csv")
        output_file = "Tao trio.csv"
        
        try:
            scraper = Scraper(
                base_url=BULBAPEDIA_URL,
                phrase="Tao trio",
                use_local_html_file=True,
                html_file_path=html_file
            )
            
            df = scraper.get_table(table_number=5, first_row_is_header=False)
            
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            with open(output_file, 'r', encoding='utf-8-sig') as f:
                generated_content = f.read()
            with open(expected_file, 'r', encoding='utf-8-sig') as f:
                expected_content = f.read()
            
            self.assertEqual(generated_content, expected_content, "Files differ!")
            
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_tao_trio_with_header(self):
        """Test Tao trio WITH --first-row-is-header (1-1 from test_tao_trio_with_header)"""
        html_file = os.path.join(TEST_DIR, "Tao trio.html")
        expected_file = os.path.join(TEST_DIR, "Tao trio flag.csv")
        output_file = "Tao trio.csv"

        try:
            scraper = Scraper(
                base_url=BULBAPEDIA_URL,
                phrase="Tao trio",
                use_local_html_file=True,
                html_file_path=html_file
            )
            
            df = scraper.get_table(table_number=5, first_row_is_header=True)
            
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            with open(output_file, 'r', encoding='utf-8-sig') as f:
                generated_content = f.read()
            with open(expected_file, 'r', encoding='utf-8-sig') as f:
                expected_content = f.read()
            
            self.assertEqual(generated_content, expected_content, "Files differ!")
            
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_string_to_windows_safe(self):
        """Test Windows-safe filename conversion (1-1 from test_string_to_windows_safe)"""
        self.assertEqual(string_to_windows_safe("Pokémon: Red"), "Pokémon- Red")
        self.assertEqual(string_to_windows_safe("Type/Water"), "Type-Water")

if __name__ == '__main__':
    unittest.main()
