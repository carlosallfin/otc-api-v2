import math
from operator import or_
from os import stat
from pyexpat import model
from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy import func, or_

router=APIRouter(
    prefix="/trades",
    tags=['Trades']
)

#Get all trades from user
@router.get("/{user_id}",status_code=status.HTTP_200_OK, response_model=schemas.TradesPagination)
def get_trades(user_id: int,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user),
    page: int=1, limit:int=10, status: str="", currency_id: int=0):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    if status=="" and currency_id==0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).count()
    if status=="" and currency_id!=0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.currency_id==currency_id).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.currency_id==currency_id).count()
    if status!="" and currency_id==0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).count()
    if status!="" and currency_id!=0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).filter(models.Trade.currency_id==currency_id).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid==0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).filter(models.Trade.currency_id==currency_id).count()
    page_size=len(trades)
    results= {'page': page,
        'total_items':total_items,
        'total_pages': math.ceil(total_items/limit),
        'page_size':page_size,
        'data':trades}
    return results

#Get all bids from user
@router.get("/bids/{user_id}",status_code=status.HTTP_200_OK, response_model=schemas.TradesPagination)
def get_trades(user_id: int,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user),
    page: int=1, limit:int=10, status: str="", currency_id: int=0):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    if status=="" and currency_id==0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).count()
    if status=="" and currency_id!=0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.currency_id==currency_id).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.currency_id==currency_id).count()
    if status!="" and currency_id==0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).count()
    if status!="" and currency_id!=0:
        trades=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).filter(models.Trade.currency_id==currency_id).limit(limit).offset((page-1)*limit).all()
        total_items=db.query(models.Trade).filter(models.Trade.is_bid!=0).filter(or_(models.Trade.owner_id==user_id,models.Trade.order_owner_id==user_id)).filter(models.Trade.status==status).filter(models.Trade.currency_id==currency_id).count()
    page_size=len(trades)
    results= {'page': page,
        'total_items':total_items,
        'total_pages': math.ceil(total_items/limit),
        'page_size':page_size,
        'data':trades}
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.TradeOut)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.active != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action. User status inactive")
    account_in=db.query(models.Account).filter(models.Account.id==trade.account_id_in).first()
    account_out=db.query(models.Account).filter(models.Account.id==trade.account_id_out).first()
    rsv_currency=db.query(models.Currency).filter(models.Currency.slug=="RSV").first()
    if not account_in:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account with id {trade.account_id_in} not found")
    if account_in.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to use this account {trade.account_id_in}")
    if not account_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account with id {trade.account_id_out} not found")
    if account_out.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Not authorized to use this account {trade.account_id_out}")
    order=db.query(models.Order).filter(models.Order.id==trade.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {trade.order_id} not found") 
    if current_user.role_id==2 and order.owner_type==2:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cannot create trade between users with role type 2") 
    if order.owner_id==current_user.id:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cannot create trade on an order created by the same user") 
    trades=db.query(models.Trade).filter(or_(models.Trade.status!='complete',models.Trade.status!='closed')).filter(models.Trade.order_id==trade.order_id).all()
    if trades:
        tradesum=sum(t.amount for t in trades)
    else:
        tradesum=0
    available=order.amount-tradesum
    if available<trade.amount:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Trade amount is greater than order available amount")
    if order.type=='sell':
        direction='buy'
        if account_in.currency_id!=rsv_currency.id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account with id {account_in.id} used to receive must be a valid RSV account")
        if account_out.currency_id!=order.currency_id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account with id {account_out.id} used to send currency's must be a the same of the order's currency id of {order.currency_id}")
    if order.type=='buy':
        direction='sell'
        if account_out.currency_id!=rsv_currency.id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account with id {account_out.id} used to send must be a valid RSV account")
        if account_in.currency_id!=order.currency_id:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account with id {account_in.id} used to receive currency's id must be a the same of the order's currency's id of {order.currency_id}")
    if current_user.role_id==1:
        collaterals=db.query(models.User, func.sum(models.Collateral.amount).label('collateral_sum')).filter(models.User.id==current_user.id).join(models.Collateral, models.Collateral.owner_id==models.User.id, isouter=True).group_by(models.User.id).first()
        orders=db.query(models.User, func.sum(models.Order.amount).label('orders_sum')).filter(models.User.id==current_user.id).filter(models.Order.status=="active").join(models.Order, models.Order.owner_id==models.User.id, isouter=True).group_by(models.User.id).first()
        trades=db.query(models.Trade).filter(models.Trade.owner_id==current_user.id).filter(or_(models.Trade.status!="complete",models.Trade.status!="closed")).all()
        if orders is None:
            sumorder=0
        else:
            sumorder=orders.orders_sum
            if sumorder is None:
                sumorder=0.00
        if collaterals in None:
            sumcollat=0
        else:
            sumcollat=collaterals.collateral_sum
            if sumcollat is None:
                sumcollat=0.00
        if trades:
            tradesum=sum(t.amount for t in trades)
        else:
            tradesum=0

        balance=sumcollat-sumorder-tradesum
        if balance<trade.amount:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'User with id: {current_user.id} does not have enough balance')
    if order.exchange_rate==trade.exchange_rate:
        bid=0
    else:
        bid=1
    new_trade=models.Trade(is_bid=bid,order_owner_id=order.owner_id,type=direction,currency_id=order.currency_id,owner_id=current_user.id,status='pending',fiat_amount=trade.amount*trade.exchange_rate,**trade.dict())
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade
    

