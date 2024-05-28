import json
import os
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def welcome():
    print("Welcome to Buff Market Scraper!")
    print("This script will scrape item data from the Buff Market website.")
    print("Please make sure you have the following dependencies installed:")
    print("selenium, beautifulsoup4, chromedriver-py")
    print("You can install them using the following command:")
    print("pip install selenium beautifulsoup4 chromedriver-py")
    print("You also need to download the ChromeDriver executable from:")
    print("https://sites.google.com/a/chromium.org/chromedriver/downloads")
    print("And place it in the same directory as this script.")


def load_driver(chromedriver_path):
    current_directory = os.getcwd()
    driver_path = os.path.join(current_directory, chromedriver_path)
    if not os.path.exists(chromedriver_path):
        print("Chromedriver not found.")
        print("Please make sure you have downloaded the ChromeDriver executable"
              " and placed it in the same directory as this script.")

    return driver_path


def link_builder(page_num, sort_by, min_price, max_price, search_term, category):
    url = f"https://buff.163.com/market/csgo#game=csgo"

    if category:
        url += f"&category_group={category}"
    if search_term:
        url += f"&search={search_term}"
    if min_price is not None:
        url += f"&min_price={min_price}"
    if max_price is not None:
        url += f"&max_price={max_price}"
    if sort_by:
        url += f"&sort_by={sort_by}"
    if page_num > 1:
        url += f"&page_num={page_num}"

    url += "&tab=selling"

    return url


def chrome_driver_config(chromedriver_path):
    # Configurar o serviço do chromedriver
    service = Service(chromedriver_path)

    # Configurar o driver do Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def add_cookies(driver, cookies):
    # Adicionar os cookies ao navegador
    for cookie in cookies:
        driver.add_cookie({'name': cookie, 'value': cookies[cookie]})


def find_max_page(chromedriver_path, cookies, url):
    driver = chrome_driver_config(chromedriver_path)
    driver.get(url)
    add_cookies(driver, cookies)
    driver.refresh()
    wait = WebDriverWait(driver, 10)

    try:
        max_page = calc_max_page(driver, wait)
    except Exception as e:
        print(f"Error: {e}")
        max_page = 1
        print("Assuming only one page of items")

    driver.quit()
    print(f"Found {max_page} pages of items")
    return int(max_page)


def calc_max_page(driver, wait):
    try:
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-link")))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        page_links = [link for link in soup.find_all("a", class_="page-link")]

        if page_links:
            max_page_test = int(page_links[-2].text)
            print(f"Max page test: {max_page_test}")
            return verify_last_page(driver, wait, max_page_test)
        else:
            return 1
    except Exception as e:
        print(f"Error while calculating max page: {e}")
        print("Assuming only one page of items")
        return 1


def verify_last_page(driver, wait, max_page):
    url_test = link_builder(max_page, config.sort_by, config.min_price, config.max_price, config.search_term,
                            config.category)
    print(f"Verifying last page: {url_test}")
    driver.get(url_test)
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-link")))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    page_links = [link for link in soup.find_all("a", class_="page-link")]
    active_page = soup.find("li", class_="active")
    if active_page:
        active_page = active_page.text
        print(f"Active page: {active_page}")
        if active_page == str(max_page):
            return max_page
    last_page = page_links[-1].text
    if last_page == "Previous page" or last_page == "Next page":
        return page_links[-2].text
    if last_page:
        print(f"Last page: {last_page}")
        return last_page
    else:
        return max_page


def scrape_items(chromedriver_path, cookies, total_pages):
    # Configurar o serviço do chromedriver
    driver = chrome_driver_config(chromedriver_path)

    # Lista para armazenar os dados extraídos
    data = []

    # Tempo de início
    start_time = time.time()

    for page_num in range(1, total_pages + 1):
        # Construir a URL com o número da página

        url = link_builder(page_num, config.sort_by, config.min_price, config.max_price, config.search_term,
                           config.category)
        print(f"Scraping page {str(page_num)}: {url}")
        # Abrir a página no navegador
        driver.get(url)

        # Adicionar os cookies ao navegador
        add_cookies(driver, cookies)

        # Recarregar a página após adicionar os cookies
        driver.refresh()

        # Esperar até que os elementos sejam carregados
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f_12px")))
        if total_pages > 1:
            time.sleep(2)
        else:
            time.sleep(4)

        # Obter o HTML da página carregada
        html = driver.page_source

        # Analisar o HTML com BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Encontrar os elementos de preços e os nomes dos itens
        items = soup.find_all("li")  # Cada item está dentro de uma tag <li>

        # Iterar sobre os itens e extrair nomes e preços
        for item in items:
            # Verificar se o item contém uma tag <h3> e uma tag <strong> com a classe f_Strong
            name_tag = item.find("h3")
            price_tag = item.find("strong", class_="f_Strong")

            if name_tag and price_tag:
                name_anchor = name_tag.find("a", title=True)
                small_tag = price_tag.find("small")
                if name_anchor:
                    item_name = name_anchor.get('title')
                    item_price = price_tag.text.replace(small_tag.text,
                                                        "") + small_tag.text if small_tag else price_tag.text.strip()

                    data.append({
                        'name': item_name,
                        'price': item_price
                    })

        # Calcular a estimativa de tempo restante
        elapsed_time = time.time() - start_time
        average_time_per_page = elapsed_time / page_num
        estimated_total_time = average_time_per_page * total_pages
        remaining_time = estimated_total_time - elapsed_time
        remaining_time_delta = timedelta(seconds=int(remaining_time))
        estimated_end_time = datetime.now() + remaining_time_delta

        # Exibir a estimativa de tempo restante
        print(f"Processed page {page_num}/{total_pages}")
        print(f"Estimated time remaining: {remaining_time_delta}")
        print(f"Estimated end time: {estimated_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=====================================")

    # Fechar o navegador
    driver.quit()

    return data


def main():
    welcome()
    # Caminho para o chromedriver (ajuste conforme necessário)
    chromedriver_path = load_driver("chromedriver.exe")

    # Carregar os cookies a partir do arquivo JSON
    with open("cookies.json") as file:
        cookies = json.load(file)
    url = link_builder(1, config.sort_by, config.min_price, config.max_price, config.search_term, config.category)
    print(f"Scraping data from {url}")
    # Número total de páginas a processar
    if config.max_pages:
        total_pages = min(config.max_pages, find_max_page(chromedriver_path, cookies, url))
        print(f"Processing {total_pages} pages")
    else:
        total_pages = find_max_page(chromedriver_path, cookies, url)

    item_data = scrape_items(chromedriver_path, cookies, total_pages)
    if not item_data:
        print('No items. Please try again with different search parameters.')
        return
    # Salvar os dados em um arquivo JSON
    if config.search_term and config.max_price is not None and config.min_price is not None:
        filename = f"{config.search_term}_{config.min_price}_{config.max_price}_data.json"
    elif config.search_term:
        filename = f"{config.search_term}_data.json"
    elif config.category:
        filename = f"{config.category}_data.json"

    else:
        filename = "item_data.json"
    with open("data/" + filename, "w", encoding="utf-8") as outfile:
        json.dump(item_data, outfile, ensure_ascii=False, indent=4)

    print("Total number of items scraped: ", len(item_data))

    print("Data saved to " + filename)


if __name__ == "__main__":
    main()
