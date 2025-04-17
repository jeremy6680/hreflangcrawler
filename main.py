import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
from urllib.parse import urljoin, urlparse
from collections import deque

def is_internal_link(href, base_netloc):
    parsed = urlparse(href)
    return (not parsed.netloc) or (parsed.netloc == base_netloc)

def crawl(base_url, max_pages=100):
    visited = set()
    data = []
    queue = deque([base_url])
    base_netloc = urlparse(base_url).netloc
    headers = {'User-Agent': 'hreflangcrawler/0.1 (+https://github.com/yourrepo)'}

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        hreflang_tags = soup.find_all('link', rel='alternate', hreflang=True)
        hreflang_dict = {tag['hreflang']: tag['href'] for tag in hreflang_tags}
        row = {'page_url': url}
        row.update(hreflang_dict)
        data.append(row)

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            if is_internal_link(full_url, base_netloc) and full_url not in visited:
                queue.append(full_url)
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <base_url>")
        sys.exit(1)
    base_url = sys.argv[1]
    data = crawl(base_url)
    df = pd.DataFrame(data)
    df.to_csv('hreflang_data.csv', index=False)