import json


def main():
    try:
        data = json.load(open("data/" + input("Enter the name of the file:") + ".json"))
        search_name(input("Enter item name:"), data)
    except FileNotFoundError:
        print("File not found")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file")


def has_key(key, data):
    return key in data


def search_name(name, data):
    for item in data:
        if 'price_brl' in item:
            if name.lower() in item['name'].lower():
                print(f"Name: {item['name']}, Price: {item['price']}, Price BRL: {item['price_brl']}")
        else:
            if name.lower() in item['name'].lower():
                print(f"Name: {item['name']}, Price: {item['price']}")
    print("Search completed")


if __name__ == "__main__":
    main()
