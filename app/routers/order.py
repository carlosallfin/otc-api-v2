from tkinter.messagebox import NO
from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/orders",
    tags=['Orders']
)

# SQL get all
# @router.get("/posts")
# def get_posts():
#     posts=cursor.execute("""SELECT * FROM posts""")
#     posts=cursor.fetchall()
#     return {'data':posts} 

# ORM get all
@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.OrdersOut])
def get_orders(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    results=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).all()
    return results
    

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.OrderCreate)
def create_orders(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.role_id==1:
        collaterals=db.query(models.User, func.sum(models.Collateral.amount)).filter(models.User.id==current_user.id).join(models.Collateral, models.Collateral.owner_id==models.User.id, isouter=True).group_by(models.User.id).first()
        orders=db.query(models.User, func.sum(models.Order.amount).label('orders_sum')).filter(models.User.id==current_user.id).filter(models.Order.status=="active").join(models.Order, models.Order.owner_id==models.User.id, isouter=True).group_by(models.User.id).first()
        sumorder=orders.orders_sum
        if sumorder is None:
            sumorder=0.00
        sumcollat=collaterals.balance
        if sumcollat is None:
            sumcollat=0.00
        balance=sumcollat-sumorder
        print(balance)
        if balance<0 or balance<order.amount:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'User with id: {current_user.id} does not have enough balance')
        
    result=db.query(models.Account).filter(models.Account.id==order.account_id).first()
    order_currency_id=result.currency_id
    new_order=models.Order(owner_id=current_user.id,currency_id=order_currency_id,current_amount=order.amount, status='active',**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
    

