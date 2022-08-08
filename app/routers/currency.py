from sqlite3 import apilevel
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models,schemas,oauth2
from database import get_db

router=APIRouter(
    prefix="/currencies",
    tags=['Currencies']
)

#ORM create user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.CurrencyCreate)
def create_currency(currency: schemas.CurrencyCreate ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    #hash password - user.password
    new_currency=models.Currency(**currency.dict())
    db.add(new_currency)
    db.commit()
    db.refresh(new_currency)

    return new_currency

