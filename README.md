# Buff Scraper

This project is a web scraper developed in Python using Selenium and BeautifulSoup to extract sales information from the CS2 market on Buff.163.com.

## Features

- Extract item names and prices listed for sale.
- Convert prices from RMB to BRL using an exchange rate API.
- Support for pagination across multiple result pages.
- Generate JSON files with the extracted data.

## Prerequisites

- Python 3.7 or higher
- Google Chrome
- Chromedriver compatible with the installed version of Google Chrome

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/buffscraper.git
    cd buffscraper
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Place the `chromedriver.exe` file in the `chromedriver-win64` folder or adjust the path in the code as needed.

## Usage

### Data Extraction

1. Set up the cookies in the `cookies.json` file.
2. Run the `main.py` script to extract the data:
    ```sh
    python buffscraper/main.py
    ```

### Currency Conversion

1. Run the `convert_currency.py` script to convert prices from RMB to BRL:
    ```sh
    python buffscraper/convert_currency.py
    ```

## Configuration

### `cookies.json` File

Cookies should be stored in a `cookies.json` file in the following format:

```json
{
    "client_Id": "cookie_value_1",
    "session": "cookie_value_2",
    "Locale-Supported": "en"
}

### config.py File

This file contains configuration variables for the scraper, such as base URL, sort_by, category, etc.

```python
# config.py

BASE_URL = "https://buff.163.com/market/csgo#game=csgo&page_num="
SORT_BY = "price.desc"
MIN_PRICE = None
MAX_PRICE = 500
SEARCH_TERM = "fallen"
CATEGORY = None
```
