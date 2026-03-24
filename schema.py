from pydantic import BaseModel, EmailStr, Field
from typing import List
from pydantic import field_validator

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

ShopName='Bolt'

class User(BaseModel):
    id: int = Field(..., gt=0, description="Azonosítónak pozitív egész számnak kell lenni!")
    name: str = Field(..., min_length=8, description="A név nem lehet üres!")
    email: EmailStr = Field(..., description="Érvényes email címet kell megadni!")
    @field_validator('id')
    def nonzero(cls,value):
        if value <= 0:
            return ValueError(f"Ez a mező nem lehet nulla! {value}")
        else:
            return value
        
class Item(BaseModel):
    item_id: int = Field(..., gt=0, description="Azonosítónak pozitív egész számnak kell lenni!")
    name: str = Field(..., min_length=3, description="A termék neve nem lehet üres!")
    brand: str = Field(..., min_length=4, description="A márka neve nem lehet üres!")
    price: float = Field(..., gt=0, description="Az árnak pozitív számnak kell lenni!")
    quantity: int = Field(..., gt=0, description="Darabszámnak pozitív egész számnak kell lenni!")
    @field_validator('item_id')
    def nonzero(cls,value):
        if value <= 0:
            return ValueError(f"Ez a mező nem lehet nulla! {value}")
        else:
            return value
        
    @field_validator('quantity')
    def nonzero(cls,value):
        if value <= 0:
            return ValueError(f"Ez a mező nem lehet nulla! {value}")
        else:
            return value    

class Basket(BaseModel):
    id: int = Field(..., gt=0, description="Kosárazonosítónak pozitív egész számnak kell lenni!")
    user_id: int = Field(..., gt=0, description="Felhasználó azonosítónak pozitív egész számnak kell lenni!")
    items: List[Item] = Field(default_factory=list, description="Termékek listája a kosárban.")

    @field_validator('id')
    def nonzero(cls,value):
        if value <= 0:
            return ValueError(f"Ez a mező nem lehet nulla! {value}")
        else:
            return value
        
    @field_validator('user_id')
    def nonzero(cls,value):
        if value <= 0:
            return ValueError(f"Ez a mező nem lehet nulla! {value}")
        else:
            return value