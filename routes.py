from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi import APIRouter
from data.filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
    delete_item
)
from data.filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try:
        user_data = user.model_dump()
        add_user(user_data)
        return JSONResponse(content=user_data)
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Nem sikerült hozzáadni a felhasználót: {str(e)}")

@routers.post('/addshoppingbag', response_model=str)
def addshoppingbag(userid: int) -> str:
    try:
        new_basket = { 
            "id": 104,  # Egyedi kosár azonosító 
            "user_id": userid,  # Az a felhasználó, akihez a kosár tartozik 
            "items": []  # Kezdetben üres kosár 
        } 
        add_basket(new_basket)
        return JSONResponse(content="Sikeres kosár hozzárendelés")
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Nem sikerült a kosár hozzáadása: {str(e)}")

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        item_data = item.model_dump()
        add_item_to_basket(userid,item_data)
        return JSONResponse(content=get_basket_by_user_id(userid))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Nem sikerült a termék hozzáadása: {str(e)}")

@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
        try:
            delete_item(userid,itemid)
            updateItem_data = updateItem.model_dump()
            add_item_to_basket(userid,updateItem_data)
            return JSONResponse(content=get_basket_by_user_id(userid))
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

@routers.delete('/deleteitem', response_model=Basket)
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        delete_item(userid,itemid)
        return JSONResponse(content=get_basket_by_user_id(userid))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.get('/user', response_model=User)
def user(userid: int) -> User:
    try:
        user = get_user_by_id(userid)
        return JSONResponse(content=user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@routers.get('/users', response_model=User)
def users() -> list[User]:
    return JSONResponse(get_all_users())

@routers.get('/shoppingbag', response_model=Basket)
def shoppingbag(userid: int) -> list[Item]:
    try:
        return JSONResponse(content=get_basket_by_user_id(userid))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/getusertotal', response_model=float)
def getusertotal(userid: int) -> float:
    try:
        return JSONResponse(get_total_price_of_basket(userid))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))