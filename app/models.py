from sqlalchemy import Column, ForeignKey,Integer,String,Boolean, Float, JSON, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# Model for table nameed post in db. 
# SQLalchemy wont modify tables if it finds a table named that way.
# Alembic for migration and changes
class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role_id = Column(Integer, nullable = False)
    active = Column(Boolean,server_default='TRUE',nullable=False)
    # balance = Column(Float, nullable=False, server_default=text('0'))
    created_at= Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Role(Base):
    __tablename__='roles'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

class Currency(Base):
    __tablename__='currencies'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
    symbol = Column(String, nullable=False, unique=True)
    input_fields = Column(ARRAY(JSON), nullable=False)

    
class Account(Base):
    __tablename__='accounts'
    id = Column(Integer,primary_key=True,nullable=False)
    user_id = Column(Integer, nullable=False)
    bank_id = Column(Integer, nullable=False)
    currency_id = Column(Integer, nullable=False)
    input_fields = Column(JSON, nullable=False)

class Bank(Base):
    __tablename__='banks'
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String, nullable=False, unique=True)
    currency_id = Column(Integer, nullable=False)

class Order(Base):
    __tablename__='orders'
    id = Column(Integer,primary_key=True,nullable=False)
    owner_id = Column(Integer, nullable = False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    life_time = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    account_id_in = Column(Integer, nullable = False)
    account_id_out = Column(Integer, nullable = False)
    bank_id = Column(Integer, nullable = False)
    owner_type=Column(Integer, nullable = False)
    currency_id = Column(Integer, nullable = False)
    
class Trade(Base):
    __tablename__='trades'
    id = Column(Integer,primary_key=True,nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    fiat_amount = Column(Float, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, nullable = False)
    account_id_in = Column(Integer, nullable = False)
    account_id_out = Column(Integer, nullable = False)
    order_id = Column(Integer, nullable = False)
    order_owner_id=Column(Integer, nullable = False)
    currency_id= Column(Integer, nullable = False)

class Payment(Base):
    __tablename__='payments'
    id = Column(Integer,primary_key=True,nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    exchange_rate = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    bank_id = Column(Integer, nullable = False)
    trade_id = Column(Integer, nullable = False)

class Collateral(Base):
    __tablename__='collaterals'
    id = Column(Integer,primary_key=True,nullable=False)
    amount = Column(Float, nullable=False)
    coin = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    status = Column(String, nullable=False, server_default=text('0'))

