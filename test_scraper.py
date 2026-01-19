from wiki_scraper import get_summary

def test_get_summary_lugia():
    expected = "Lugia (Japanese: ルギア Lugia) is a dual-type Psychic/Flying Legendary Pokémon introduced in Generation II."
    result = get_summary("Lugia")
    assert result == expected

def test_get_summary_not_found():
    phrase = "gdagdaga"
    expected = f"Error: Article for '{phrase}' not found on Bulbapedia."
    result = get_summary(phrase)
    assert result == expected
