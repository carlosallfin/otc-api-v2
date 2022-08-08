from dataclasses import fields
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models,schemas,oauth2
from database import get_db
import json

router=APIRouter(
    prefix="/accounts",
    tags=['accounts']
)

#ORM create account
# @router.get("/", status_code=status.HTTP_201_CREATED,response_model=schemas.AccountCreate)
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.AccountCreate)

def create_account(account: schemas.AccountCreate ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    received_input_fields=account.input_fields
    account_input_fields={}
    currency=db.query(models.Currency).filter(models.Currency.id==account.currency_id).first()
    currency_data = currency.input_fields
    errors_in_fields=[]
    for c in currency_data:
        c['found']=False
        if c['title'] in received_input_fields.keys():
            c['found']=True
            if len(received_input_fields[c['title']])>=c['min'] and len(received_input_fields[c['title']])<=c['max']:
                account_input_fields[c['title']]=received_input_fields[c['title']]
            else:
                errors_in_fields.append(f"key: {c['title']} input: {received_input_fields[c['title']]} min: {c['min']} max: {c['max']}")
    missing_fields=[]
    for c in currency_data:
        if c['found']==False:
            missing_fields.append(c['title'])
    if missing_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Did not receive data: {missing_fields}")
    if errors_in_fields:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f"Errors in fields: {errors_in_fields}")
    account.input_fields=account_input_fields
    new_account=models.Account(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/{user_id}/{currency_id}", status_code=status.HTTP_200_OK)

def get_user_accounts(user_id:int,currency_id:int, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    accounts=db.query(models.Account).filter(models.Account.user_id==user_id).filter(models.Account.currency_id==currency_id).all()
    return accounts
