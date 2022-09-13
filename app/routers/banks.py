from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import get_db
from typing import List

router=APIRouter(
    prefix="/banks",
    tags=['Banks']
)

#ORM create account
# @router.get("/", status_code=status.HTTP_201_CREATED,response_model=schemas.AccountCreate)
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Banks])

def get_all(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    banks=db.query(models.Bank).all()
    return banks

@router.get("/{currency_id}", status_code=status.HTTP_200_OK, response_model=List[schemas.Banks])

def get_all_by_currency(currency_id:int, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    banks=db.query(models.Bank).filter(models.Bank.currency_id==currency_id).all()
    return banks

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.BankCreate)

def get_account(bank: schemas.BankCreate ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    #hash password - user.password
    new_bank=models.Bank(**bank.dict())
    db.add(new_bank)
    db.commit()
    db.refresh(new_bank)

    return new_bank
