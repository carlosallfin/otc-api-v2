from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user, auth, currency, accounts, banks, order, trade
from .config import settings

# Creates all of our models
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins=["http://otcrsv.livingcodestudio.com/","http://otcrsv.livingcodestudio.com","https://otcrsv.livingcodestudio.com/","https://otcrsv.livingcodestudio.com","http://localhost:3000","http://localhost","http://localhost:3000/","https://207.244.246.57","http://207.244.246.57"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(currency.router)
app.include_router(accounts.router)
app.include_router(banks.router)
app.include_router(order.router)
app.include_router(trade.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
