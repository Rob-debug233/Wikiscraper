import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json

def string_to_windows_safe(text):
    unsafe_chars = r':<>"/\|?*'
    safe_text = text
    for char in unsafe_chars:
        safe_text = safe_text.replace(char, '-')
    return safe_text

def get_soup_from_url(url):
    """
    Pobiera treść strony z podanego adresu URL i zwraca obiekt BeautifulSoup.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException:
        return None

def get_soup_from_file(filepath):
    """
    Wczytuje HTML z pliku lokalnego i zwraca obiekt BeautifulSoup.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

class Scraper:
    """
    Scraper do pobierania danych z Bulbapedii.
    Wspiera zarówno pobieranie online jak i offline z plików HTML.
    """
    
    def __init__(self, base_url, phrase, use_local_html_file=False, html_file_path=None, html_content=None):
        """
        Inicjalizuje scraper.
        
        Args:
            base_url: Bazowy URL (np. "https://bulbapedia.bulbagarden.net/wiki/")
            phrase: Fraza do wyszukania (np. "Team Rocket")
            use_local_html_file: Czy czytać z pliku zamiast pobierać
            html_file_path: Ścieżka do pliku HTML (jeśli use_local_html_file=True)
            html_content: Bezpośrednia zawartość HTML jako string
        """
        self.base_url = base_url
        self.phrase = phrase
        self.use_local_html_file = use_local_html_file
        self.html_file_path = html_file_path
        self.html_content = html_content
        self.soup = None
        
        # Załaduj HTML
        if self.html_content:
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
        elif self.use_local_html_file and self.html_file_path:
            self.soup = get_soup_from_file(self.html_file_path)
        else:
            url = f"{self.base_url}{self.phrase.replace(' ', '_')}"
            self.soup = get_soup_from_url(url)
    
    def get_summary(self):
        """
        Pobiera pierwsze akapity ze strony.
        """
        if not self.soup:
            return "Error: Could not load page."
        
        for p in self.soup.find_all('p'):
            text = p.get_text().strip()
            if text:
                return text
        return "Error: No summary found."
    
    def get_table(self, table_number, first_row_is_header=True):
        """
        Pobiera tabelę ze strony i zwraca DataFrame.
        """
        tables = self.soup.find_all('table')
        target_table = tables[table_number - 1]
        
        rows = []
        for tr in target_table.find_all('tr'):
            cells = tr.find_all(['th', 'td'])
            row_data = [cell.get_text(separator=" ", strip=True) for cell in cells]
            if row_data:
                rows.append(row_data)

        # Normalizuj liczbę kolumn
        max_columns = max(len(row) for row in rows)
        normalized_rows = [row + [""] * (max_columns - len(row)) for row in rows]
        
        if first_row_is_header:
            df = pd.DataFrame(normalized_rows[1:], columns=normalized_rows[0])
        else:
            df = pd.DataFrame(normalized_rows)
        
        return df

def save_dataframe_to_csv(df, phrase):
    """
    Zapisuje DataFrame do pliku CSV.
    """
    safe_filename = string_to_windows_safe(phrase)
    filename = f"{safe_filename}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Table saved to {filename}")

def analyze_frequency(df, phrase):
    """
    Wyświetla analizę częstości wartości w DataFrame.
    """
    print("\nValue Frequency Analysis:")
    freq = df.stack().value_counts()
    print(freq.to_string())

def get_word_count_from_json(filepath):
    """
    Suma wszystkie wartości (counts) z podanego pliku JSON.
    """
    if not os.path.exists(filepath):
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return sum(data.values())
