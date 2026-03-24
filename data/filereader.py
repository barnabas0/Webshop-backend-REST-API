import json
from typing import Dict, Any, List

'''
Útmutató a féjl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = "D:\\Egyetem\\2024-25-2\\Python\\Beadandó1\\API\\data\\data.json"

def load_json() -> Dict[str, Any]: 
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data

data = load_json()

def get_user_by_id(user_id: int) -> Dict[str, Any]:  
    for user in data["Users"]:
        if user["id"] == user_id:
            return user
    raise ValueError(f"Nem létezik felhasználó az adott azonosítóval! id:{user_id}")

def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            return basket
    raise ValueError(f"Nem létezik kosár a megadott felhasználó azonosítóval! user_id:{user_id}")

def get_all_users() -> List[Dict[str, Any]]:
    return data["Users"]

def get_total_price_of_basket(user_id: int) -> float:
    if any(basket["user_id"] == user_id for basket in data["Baskets"]):
        sum = 0
        basket = get_basket_by_user_id(user_id)
        for item in basket:
            sum += item["price"]
        return sum
    else:
        raise ValueError(f"Nem létezik kosár a megadott felhasználó azonosítóval! user_id:{user_id}")
