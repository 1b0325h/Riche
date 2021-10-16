# Riche

When you search in the search box, Google search results are scraped and displayed. Since the scraping accesses each page to get the title and snippet, it takes time for the results to appear.

## Requirements

- Python3.8+
- Python Libraries
  - `pip install -r requirements.txt`
- Sass
  - `choco install sass`

## Usage

1. Run `python app.py` to run the server locally on your machine.
2. Open `localhost:50000` to view it in the browser.

If you prefix your search keyword with `?` at the beginning of a search term will redirect you to Google search results page.  
`!` You can use DuckDuckGo Bang command to redirect to DuckDuckGo search results page.
