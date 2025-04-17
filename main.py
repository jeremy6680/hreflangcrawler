import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python main.py <base_url>")
    sys.exit(1)

base_url = sys.argv[1]
visited = set()
data = []

def crawl(url):
    if url in visited or len(visited) >= 100:  # limit to 100 pages
        return
    
    visited.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    hreflang_tags = soup.find_all('link', rel='alternate', hreflang=True)
    hreflang_dict = {tag['hreflang']: tag['href'] for tag in hreflang_tags}

    # Initialize the row with the page URL
    row = {'page_url': url}
    row.update(hreflang_dict)
    data.append(row)

    # Find all internal links and crawl them
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/') or href.startswith(base_url):
            full_url = href if href.startswith(base_url) else base_url + href
            crawl(full_url)

crawl(base_url)

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('hreflang_data.csv', index=False)