import json
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from wordfreq import word_frequency, get_frequency_dict
from collections import Counter

WORD_COUNTS_FILE = "word-counts.json"

WORD_COUNTS_FILE = "word-counts.json"

def get_word_counts():
    """Wczytuje licznik słów z pliku JSON."""
    if not os.path.exists(WORD_COUNTS_FILE):
        return Counter()
    with open(WORD_COUNTS_FILE, 'r', encoding='utf-8') as f:
        return Counter(json.load(f))

def normalize_frequencies(df, col_name):
    """Normalizuje kolumnę dzieląc przez wartość maksymalną (skala 0-1)."""
    max_val = df[col_name].max()
    if max_val > 0:
        df[col_name] = df[col_name] / max_val
    return df

def get_wiki_language_frequency(word, lang='en'):
    """Zwraca częstotliwość słowa w danym języku (biblioteka wordfreq)."""
    return word_frequency(word, lang)

def analyze_relative_frequency(mode, count_n, chart_path=None, lang='en'):
    """Analizuje częstotliwość słów artykułu na tle całego języka."""
    article_counts = get_word_counts()
    
    if not article_counts:
        print("Nie znaleziono danych. Uruchom najpierw --count-words.")
        return

    df_article = pd.DataFrame.from_dict(article_counts, orient='index', columns=['raw_count']).reset_index()
    df_article.columns = ['word', 'raw_count']
    
    total_words_article = df_article['raw_count'].sum()
    df_article['frequency in the article'] = df_article['raw_count'] / total_words_article
    df_article['frequency in wiki language'] = df_article['word'].apply(get_wiki_language_frequency, lang=lang)
    
    # Obsługa słów, których nie ma w słowniku języka
    mask_missing_words = df_article['frequency in wiki language'] == 0.0
    df_article.loc[mask_missing_words, 'frequency in wiki language'] = float('nan')

    if mode == 'article':
        df_sorted = df_article.sort_values(by='frequency in the article', ascending=False)
        df_final = df_sorted.head(count_n).copy()
        
    elif mode == 'language':
        from wordfreq import top_n_list
        # Pobieramy więcej słów na wypadek braków w dopasowaniu
        top_lang_words = top_n_list(lang, count_n * 2) 
        
        df_lang = pd.DataFrame(top_lang_words, columns=['word'])
        df_lang['frequency in wiki language'] = df_lang['word'].apply(get_wiki_language_frequency, lang=lang)
        
        df_merged = pd.merge(df_lang, df_article[['word', 'frequency in the article']], on='word', how='left')
        df_sorted = df_merged.sort_values(by='frequency in wiki language', ascending=False)
        df_final = df_sorted.head(count_n).copy()

    else:
        print(f"Nieznany tryb: {mode}")
        return

    df_final = normalize_frequencies(df_final, 'frequency in the article')
    df_final = normalize_frequencies(df_final, 'frequency in wiki language')

    print("\n--- Analiza Częstotliwości Słów (Normalized) ---")
    cols_to_show = ['word', 'frequency in the article', 'frequency in wiki language']
    print(df_final[cols_to_show].to_string(index=False))

    if chart_path:
        df_chart = df_final.fillna(0.0)
        generate_chart(df_chart, chart_path, count_n)

def generate_chart(df, chart_path, n):
    """Generuje wykres słupkowy i zapisuje go do pliku."""
    if df.empty:
        print("Brak danych do wygenerowania wykresu.")
        return

    chart_data = df.head(n).copy()
    words_list = chart_data['word']
    x_positions = range(len(words_list))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    pos_left = [i - bar_width/2 for i in x_positions]
    pos_right = [i + bar_width/2 for i in x_positions]
    
    ax.bar(pos_left, chart_data['frequency in the article'], bar_width, label='Częstotliwość w artykule', color='blue')
    ax.bar(pos_right, chart_data['frequency in wiki language'], bar_width, label='Częstotliwość w języku wiki', color='red')

    ax.set_ylabel('Znormalizowana częstotliwość')
    ax.set_title(f'Częstotliwość top {n} słów: Wiki vs Język')
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(words_list, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    plt.savefig(chart_path)
    print(f"Wykres zapisano do: {chart_path}")
    plt.close()

if __name__ == "__main__":
    # Do testów manualnych
    pass
