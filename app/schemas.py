from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, conint, conlist, Json
from datetime import datetime

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

class CurrencyCreate(BaseModel):
    name:str
    slug: str
    symbol: str
    input_fields: conlist(Dict,min_items=2)
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
    access_token: str
    token_type: str

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
    user_id:int
    bank_id: int
    currency_id: int
    input_fields: Dict
    class Config:
        orm_mode=True

class BankCreate(BaseModel):
    name: str
    currency_id: int
    class Config:
        orm_mode=True