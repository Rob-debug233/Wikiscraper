def lang_confidence_score(word_counts, language_words_with_frequency):
    """
    Oblicza stopień pewności języka na podstawie pokrycia słów.
    
    Prosta idea: Jeśli tekst jest w danym języku, większość jego słów 
    powinna być wśród najczęstszych słów tego języka.
    
    Score = (liczba wystąpień słów z top-k / wszystkie słowa) * 100
    
    Args:
        word_counts (dict): Słownik {słowo: liczba} z tekstu.
        language_words_with_frequency (dict): Słownik {słowo: częstość} 
                                              dla top-k słów języka docelowego.
                                               
    Returns:
        float: Score pokrycia (0-100). Wyższy = lepsze dopasowanie.
    """
    if not word_counts:
        return 0.0
        
    total_words = sum(word_counts.values())
    if total_words == 0:
        return 0.0
    
    # Zlicz ile wystąpień słów jest pokrytych przez top-k słów języka
    covered_count = 0
    for word, count in word_counts.items():
        if word in language_words_with_frequency:
            covered_count += count
    
    # Zwróć procent pokrycia
    coverage_score = (covered_count / total_words) * 100
    return coverage_score
