# Riche

Simplify your search results with the Custom Search API.

## Requirements

- Python3.8+
- Python Libraries
  - `pip install -r requirements.txt`
- Sass
  - `choco install sass`

## Usage

1. Getting Google API key and activating Custom Search API.
2. Rename `.env.example` to `.env` and set `<GOOGLE_API_KEY>` and `<CUSTOM_SEARCH_ENGINE_ID>.`
3. Run `python app.py` to run the server locally on your machine.
4. Open `localhost:50000` to view it in the browser.

### Startup

Adding it to Startup will run in the background when PC is started.

1. Open the startup folder by type `shell:startup` in the Windows search.
2. Just put `Riche.vbs` there.

### How to search

Type in the search box and Enter to simply display results. If you prefix your search keyword with `?` at the beginning of a search term will redirect you to Google search results page. `!` You can use DuckDuckGo Bang command to redirect to DuckDuckGo search results page.
