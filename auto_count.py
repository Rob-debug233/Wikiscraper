import time
import urllib.parse
from collections import deque
from utils import Scraper
from count import count_words_from_html, update_word_counts

def extract_wiki_links(soup):
    """
    Extracts wiki links from the main content area.
    Only includes links that point to other /wiki/ articles and are not special pages.
    """
    if not soup:
        return []
    
    content = soup.find('div', id='mw-content-text')
    if not content:
        return []
    
    links = []
    for a in content.find_all('a', href=True):
        href = a['href']
        # Check if it's a wiki link
        if href.startswith('/wiki/') and ':' not in href:
            # Extract the phrase from the URL and decode it
            phrase_quoted = href.replace('/wiki/', '')
            phrase = urllib.parse.unquote(phrase_quoted).replace('_', ' ')
            # Handle anchor links
            phrase = phrase.split('#')[0]
            if phrase and phrase not in links:
                links.append(phrase)
    
    return links

def auto_count_bfs(base_url, start_phrase, max_depth, wait_time):
    """
    Performs a BFS crawl starting from start_phrase up to max_depth.
    """
    queue = deque([(start_phrase, 0)])
    visited = {start_phrase}
    
    while queue:
        current_phrase, current_depth = queue.popleft()
        
        scraper = Scraper(base_url, current_phrase)
        
        if scraper.soup:
            word_counter = count_words_from_html(scraper.soup)
            if word_counter:
                update_word_counts(word_counter)
        
        if current_depth < max_depth and scraper.soup:
            new_links = extract_wiki_links(scraper.soup)
            for link in new_links:
                if link not in visited:
                    visited.add(link)
                    queue.append((link, current_depth + 1))
        
        if queue and wait_time > 0:
            time.sleep(wait_time)