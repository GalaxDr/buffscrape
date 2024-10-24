"""
This script is used to save the cookies to a file.
It will prompt the user for the client_id and session cookies, and save them to a file named cookies.json.
"""
import json

client_id = input("Enter your client_id: ")
session = input("Enter your session: ")

cookies = {
    "client_id": client_id,
    "session": session,
    "Locale-Supported": "en"
}

with open("cookies.json", "w", encoding="utf-8") as file:
    json.dump(cookies, file, ensure_ascii=False, indent=4)

print("Cookies saved to cookies.json")
