from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserOut(BaseModel):
    id:str
    name: str
    email: EmailStr
    created_at:datetime
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

class CurrencyOut(BaseModel):
    id: int
    name:str
    slug: str
    symbol: str
    class Config:
        orm_mode=True

class BankOut(BaseModel):
    id: int
    name:str
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

class AccountOut(BaseModel):
    id: int
    currency_info: CurrencyOut
    bank_info: BankOut
    input_fields: Dict
    class Config:
        orm_mode=True

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

class TradeOrderOut(BaseModel):
    id: int
    type: str
    exchange_rate: float
    account_in: AccountOut
    account_out: AccountOut
    created_at: datetime
    life_time: float
    class Config:
        orm_mode=True

class TradeOrderUserOut(BaseModel):
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

class TradeOut(TradeOrderUserOut):
    order_info: TradeOrderOut

class CreateTradeOut(BaseModel):
    id: int
    owner_id: int
    order_id: int
    type: str
    amount: float
    fiat_amount: float
    exchange_rate: float
    status: str
    account_in: AccountOut
    account_out: AccountOut
    created_at: datetime
    currency_id: int
    class Config:
        orm_mode=True

class OrderBookOut(BaseModel):
    id: int
    owner_id: int
    type: str
    amount: float
    exchange_rate: float
    status: str
    currency_id: int
    bank_id: int
    owner_type: int
    created_at: datetime
    life_time: float
    available: float 
    class Config:
        orm_mode=True

class OrderOut(OrderBookOut):
    account_in: AccountOut
    account_out: AccountOut

class OrderUserOut(OrderOut):
    trades: List[TradeOrderUserOut]

class Pagination(BaseModel):
    page: int
    total_items: int
    total_pages: int
    page_size: int
    data: List[OrderOut]
    class Config:
        orm_mode=True

class OrdersPagination(Pagination):
    data: List[OrderOut]

class OrdersBookPagination(Pagination):
    data: List[OrderBookOut]

class TradesPagination(Pagination):
    data: List[TradeOut]

class OrdersUserPagination(Pagination):
    data: List[OrderUserOut]

class OrderSeparate(BaseModel):
    buy: OrdersBookPagination
    sell: OrdersBookPagination
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





