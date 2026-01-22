#python -m pytest test_scraper.py -v

import json
import os
import pandas as pd
from utils import Scraper, string_to_windows_safe
from count import count_words_for_phrase, WORD_COUNTS_FILE

TEST_DIR = "test"
BULBAPEDIA_URL = "https://bulbapedia.bulbagarden.net/wiki/"

def test_word_counts_accumulation():
    """Test zliczania słów i akumulacji w word-counts.json"""
    reference_file = os.path.join(TEST_DIR, "word-counts_Type_two_times.json")
    
    if os.path.exists(WORD_COUNTS_FILE):
        os.remove(WORD_COUNTS_FILE)
    
    try:
        # Policz dwa razy dla frazy "Type"
        count_words_for_phrase(BULBAPEDIA_URL, "Type")
        count_words_for_phrase(BULBAPEDIA_URL, "Type")
        
        with open(WORD_COUNTS_FILE, 'r', encoding='utf-8') as f:
            generated_data = json.load(f)
        with open(reference_file, 'r', encoding='utf-8') as f:
            reference_data = json.load(f)
            
        assert generated_data == reference_data, "Wygenerowane statystyki słów różnią się!"
        
    finally:
        if os.path.exists(WORD_COUNTS_FILE):
            os.remove(WORD_COUNTS_FILE)

def test_summary_offline():
    """Test get_summary z lokalnego pliku HTML"""
    html_file = os.path.join(TEST_DIR, "Lugia.html")
    
    scraper = Scraper(
        base_url=BULBAPEDIA_URL,
        phrase="Lugia",
        use_local_html_file=True,
        html_file_path=html_file
    )
    
    result = scraper.get_summary()
    assert result == "Lugia (Japanese: ルギア Lugia) is a dual-type Psychic/Flying Legendary Pokémon introduced in Generation II."

def test_summary_not_found():
    """Test get_summary dla artykułu który nie istnieje"""
    scraper = Scraper(
        base_url=BULBAPEDIA_URL,
        phrase="adgadadagdasg"
    )
    
    result = scraper.get_summary()
    assert result == "Error: Could not load page."

def test_tao_trio_without_header():
    """Test Tao trio BEZ --first-row-is-header - porównaj z test/Tao trio without flag.csv"""
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
        
        assert generated_content == expected_content, f"Pliki się różnią!\n\nGenerated:\n{generated_content}\n\nExpected:\n{expected_content}"
        
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def test_tao_trio_with_header():
    """Test Tao trio Z --first-row-is-header - porównaj z test/Tao trio flag.csv"""
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
        
        assert generated_content == expected_content, f"Pliki się różnią!"
        
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)


def test_string_to_windows_safe():
    """Test konwersji nazw na format Windows-safe"""
    assert string_to_windows_safe("Pokémon: Red") == "Pokémon- Red"
    assert string_to_windows_safe("Type/Water") == "Type-Water"