from locale import currency
from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr, conint, conlist
from datetime import datetime

from .models import Currency

class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:str
    name: str
    email: EmailStr
    created_at:datetime
    class Config:
        orm_mode=True

class Post(PostBase):
    id: int
    created_at:datetime
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode=True

class InputFieldsCurrency(BaseModel):
    title: str
    min: int
    max: int
    class Config:
        orm_mode=True

class CurrencyCreate(BaseModel):
    name:str
    slug: str
    symbol: str
    input_fields: List[InputFieldsCurrency]
    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role_id: conint(ge=0, le=2)
    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    logged: bool
    detail: str
    access_token: str
    token_type: str
    user_data: Dict

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Role(BaseModel):
    id: int
    name: str
    slug: str
    description: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role_id: conint(ge=0, le=2)
    class Config:
        orm_mode=True

class CollateralCreate(BaseModel):
    amount: float
    owner_id: int
    status: str
    class Config:
        orm_mode=True

class UserOutColl(BaseModel):
    id:str
    name: str
    email: EmailStr
    balance: float
    class Config:
        orm_mode=True

class AccountCreate(BaseModel):
    bank_id: int
    currency_id: int
    input_fields: Dict
    class Config:
        orm_mode=True

class AccountOut(AccountCreate):
    id: int

class BankCreate(BaseModel):
    name: str
    currency_id: int
    class Config:
        orm_mode=True

class OrderCreate(BaseModel):
    type: str
    amount: float
    exchange_rate: float    
    life_time: float
    account_id_in: int
    account_id_out: int
    class Config:
        orm_mode=True

class TradeCreate(BaseModel):
    order_id: int
    amount: float
    exchange_rate: float
    account_id_in: int
    account_id_out: int
    class Config:
        orm_mode=True

class TradeOut(BaseModel):
    id: int
    owner_id: int
    order_id: int
    type: str
    amount: float
    fiat_amount: float
    exchange_rate: float
    status: str
    owner_id: int
    account_in: AccountOut
    account_out: AccountOut
    created_at: datetime
    currency_id: int
    class Config:
        orm_mode=True



class OrderOut(BaseModel):
    id: int
    owner_id: int
    type: str
    amount: float
    exchange_rate: float
    status: str
    currency_id: int
    account_in: AccountOut
    account_out: AccountOut
    bank_id: int
    owner_type: int
    created_at: datetime
    life_time: float
    class Config:
        orm_mode=True

class OrderUserOut(OrderOut):
    trades: List[TradeOut]

class OrdersPagination(BaseModel):
    page: int
    total_items: int
    total_pages: int
    page_size: int
    data: List[OrderOut]
    class Config:
        orm_mode=True

class TradesPagination(BaseModel):
    page: int
    total_items: int
    total_pages: int
    page_size: int
    data: List[TradeOut]
    class Config:
        orm_mode=True

class OrdersUserPagination(BaseModel):
    page: int
    total_items: int
    total_pages: int
    page_size: int
    data: List[OrderUserOut]
    class Config:
        orm_mode=True


class OrderSeparate(BaseModel):
    buy: OrdersPagination
    sell: OrdersPagination
    class Config:
        orm_mode=True

class OrdersOut(BaseModel):
    Order: OrderOut
    available_balance: float 
    class Config:
        orm_mode=True

class OrdersOutTrades(OrderOut):
    trades: List[TradeOut]

class OrdersOutUser(BaseModel):
    Order: OrdersOutTrades
    available_balance: float 
    class Config:
        orm_mode=True
    

class Users(BaseModel):
    User: UserOut
    available_balance: float 
    class Config:
        orm_mode=True

class Banks(BankCreate):
    id: int

class Currency(CurrencyCreate):
    id: int





