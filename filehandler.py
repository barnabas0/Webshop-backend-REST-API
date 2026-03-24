import json
from typing import Dict, Any
from data.filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = "D:\\Egyetem\\2024-25-2\\Python\\Beadandó1\\API\\data\\data.json"

def load_json() -> Dict[str, Any]:
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

data = load_json()

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH,'w') as file:
        json.dump(data,file,indent=4)

def add_user(user: Dict[str, Any]) -> None:
    used_ids = {user["id"] for user in data["Users"]}
    if user["id"] not in used_ids:
        data["Users"].append(user)
        save_json(data)
    else:
       raise ValueError("Nem lehet két azonos id-val rendelkező felhasználó!") 

def add_basket(basket: Dict[str, Any]) -> None:
    used_basket_ids = {basket["id"] for basket in data["Baskets"]}
    if basket["id"] not in used_basket_ids:
        data["Baskets"].append({"id": basket["id"], "user_id": basket["user_id"], "items": basket["items"]})
        save_json(data)
    else:
        raise ValueError("Nem lehet két azonos id-val rendelkező kosár!")

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    existing_basket_user_ids = {basket["user_id"] for basket in data["Baskets"]}
    if user_id not in existing_basket_user_ids:
        raise ValueError("Nem található kosár az adott felhasználó azonosítóval!")
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket["items"].append(item)
            save_json(data)

def delete_item(user_id: int, item_id: int) -> None:
    existing_basket_user_ids = {basket["user_id"] for basket in data["Baskets"]}
    if user_id not in existing_basket_user_ids:
        raise ValueError("Nem található kosár az adott felhasználó azonosítóval!")
    basket = get_basket_by_user_id(user_id)
    items = basket["items"]
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket["items"] = [item for item in items if item["item_id"] != item_id]
            save_json(data)
