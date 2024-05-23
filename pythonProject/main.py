import json
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Caminho para o chromedriver (ajuste conforme necessário)
chromedriver_path = 'C:/Users/julio/Desktop/codes/buffscrape/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Configurar o serviço do chromedriver
service = Service(chromedriver_path)

# Configurar o driver do Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Carregar os cookies a partir do arquivo JSON
with open("cookies.json") as file:
    cookies = json.load(file)

# Número total de páginas a processar
total_pages = 2

# Lista para armazenar os dados extraídos
data = []

# Tempo de início
start_time = time.time()

for page_num in range(1, total_pages + 1):
    # Construir a URL com o número da página
    url = f"https://buff.163.com/market/csgo#game=csgo&page_num={page_num}&tab=selling"

    # Abrir a página no navegador
    driver.get(url)

    # Adicionar os cookies ao navegador
    for cookie in cookies:
        driver.add_cookie({'name': cookie, 'value': cookies[cookie]})

    # Recarregar a página após adicionar os cookies
    driver.refresh()

    # Esperar até que os elementos sejam carregados
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "f_12px")))

    # Obter o HTML da página carregada
    html = driver.page_source

    # Analisar o HTML com BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Encontrar os elementos de preços e os nomes dos itens
    items = soup.find_all("li")  # Cada item está dentro de uma tag <li>

    # Iterar sobre os itens e extrair nomes e preços
    for item in items:
        name_tag = item.find("a", title=True)
        price_tag = item.find("span", class_="f_12px")

        if name_tag and price_tag:
            item_name = name_tag.get('title')
            item_price = price_tag.text.strip()
            data.append({
                'name': item_name,
                'price': item_price
            })
    time.sleep(1)  # Aguardar 1 segundo antes de prosseguir para a próxima página
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

# Fechar o navegador
driver.quit()

# Salvar os dados em um arquivo JSON
with open("item_data.json", "w") as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Data saved to item_data.json")
