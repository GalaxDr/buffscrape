# -*- coding: utf-8 -*-
import json
import requests


def convert_rmb_to_brl(rmb, exchange_rate):
    # Converta o preço de string para float
    price_number = float(rmb.replace("¥", "").strip())

    # Obtenha a taxa de câmbio atual de RMB para BRL
    brl_price = price_number * exchange_rate

    # Converta o preço de RMB para BRL usando a taxa de câmbio
    return format(brl_price, ".2f")


def main():
    data_file = input("Enter the name of the file (without .json extension): ") + "_data.json"
    # Obtenha a taxa de câmbio atual de RMB para BRL
    url = "https://api.exchangerate-api.com/v4/latest/CNY"
    response = requests.get(url)
    data = response.json()
    exchange_rate = data['rates']['BRL']
    try:
        # Abra e leia o arquivo JSON de entrada
        with open("data/" + data_file, "r", encoding="utf-8") as file:
            currencies = json.load(file)
    except FileNotFoundError:
        print("File not found")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON from the file")
        return

    for currency in currencies:
        # Converta o preço para BRL e atualize o dicionário
        currency['price_brl'] = "R$ " + convert_rmb_to_brl(currency['price'], exchange_rate)

    # Salve os dados convertidos em um novo arquivo JSON
    output_file = data_file.replace(".json", "_to_brl.json")
    with open("data/" + output_file, "w", encoding="utf-8") as file:
        json.dump(currencies, file, ensure_ascii=False, indent=4)

    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()
