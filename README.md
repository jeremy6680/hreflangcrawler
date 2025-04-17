# Hreflang Crawler

Hreflang Crawler is a simple Python script that crawls a website, extracts all `<link rel="alternate" hreflang="...">` tags from up to 100 pages, and exports the results to a CSV file. This is useful for auditing hreflang implementations across a website for SEO purposes.

## Features

- Recursively crawls internal links starting from a base URL (up to 100 pages).
- Extracts all hreflang tags and their corresponding URLs from each page.
- Outputs a CSV file (`hreflang_data.csv`) with the collected data.

## Requirements

- Python 3.12+
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [pandas](https://pypi.org/project/pandas/)

Install dependencies with:

```sh
pip install -r requirements.txt
```

Or, if using `pyproject.toml`:

```sh
pip install .
```

## Usage

Run the script from the command line, providing the base URL to crawl. For example:

```sh
python main.py https://example.com
```

- The script will crawl up to 100 internal pages starting from the base URL.
- It will extract all hreflang tags from each page.
- Results are saved to `hreflang_data.csv` in the current directory.

## Output

The output CSV will have one row per crawled page, with columns for the page URL and each found hreflang value:

| page_url           | en  | fr  | de  | ... |
|--------------------|-----|-----|-----|-----|
| https://.../page1  | ... | ... | ... | ... |
| https://.../page2  | ... | ... | ... | ... |

## Notes

- Only internal links (same domain or relative URLs) are followed.
- The crawl is limited to 100 pages to avoid excessive requests.
- Make sure you have permission to crawl the target website.

## License

MIT License