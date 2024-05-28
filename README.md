# Buff Scraper

Este projeto é um web scraper desenvolvido em Python, utilizando Selenium e BeautifulSoup, para extrair informações de itens de venda do mercado de CS2 no site Buff.163.com.

## Funcionalidades

- Extrair nomes e preços de itens listados para venda.
- Conversão de preços de RMB para BRL usando uma API de taxa de câmbio.
- Suporte para paginação de múltiplas páginas de resultados.
- Geração de arquivos JSON com os dados extraídos.

## Pré-requisitos

- Python 3.7 ou superior
- Google Chrome
- Chromedriver compatível com a versão do Google Chrome instalada

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/buffscraper.git
    cd buffscraper
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Coloque o arquivo `chromedriver.exe` na pasta `chromedriver-win64` ou ajuste o caminho no código conforme necessário.

## Uso

### Extração de Dados

1. Configure os cookies no arquivo `cookies.json`.
2. Execute o script `main.py` para extrair os dados:
    ```sh
    python buffscraper/main.py
    ```

### Conversão de Moeda

1. Execute o script `convert_currency.py` para converter os preços de RMB para BRL:
    ```sh
    python buffscraper/convert_currency.py
    ```

## Configuração

### Arquivo `cookies.json`

Os cookies devem ser armazenados em um arquivo cookies.json no seguinte formato:

```json
{
    "client_Id": "cookie_value_1",
    "session": "cookie_value_2",
    "Locale-Supported": "en"
}
```

### Arquivo `config.py`

Este arquivo contém variáveis de configuração para o scraper, como URL base, sort_by, categoria, etc.

```python
# config.py

base_url = "https://buff.163.com/market/csgo#game=csgo&page_num="
sort_by = "price.desc"
min_price = None
max_price = 500
search_term = "fallen"
category = None
