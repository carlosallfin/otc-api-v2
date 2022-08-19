import math
from operator import or_
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


# ORM get all
@router.post("/test",status_code=status.HTTP_201_CREATED)
def create_trades(db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user),
    currency: int=0, bank:int=0, separate: bool=False,page: int=1, limit:int=10, page_buy: int=1, page_sell: int=1):
    if separate==False:
        if currency==0 and bank==0:
            results=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).limit(limit).offset((page-1)*limit).all()
            total_items=db.query(models.Order).count()
        if currency!=0 and bank==0:
            results=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.currency_id==currency).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).limit(limit).offset((page-1)*limit).all()
            total_items=db.query(models.Order).filter(models.Order.currency_id==currency).count()
        if currency!=0 and bank != 0:
            results=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.currency_id==currency).filter(models.Order.bank_id==bank).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).limit(limit).offset((page-1)*limit).all()
            total_items=db.query(models.Order).filter(models.Order.currency_id==currency).filter(models.Order.currency_id==currency).filter(models.Order.bank_id==bank).count()
        if currency==0 and bank != 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= "You must filter by currency first to filter by bank")
        orders=[]
        for r in results:
            order=r.Order
            order.availabe=r.available_balance
            orders.append(order)
        page_size=len(orders)
        for o in orders:
            trades=db.query(models.Trade).filter(models.Trade.order_id==o.id).all()
            o.trades=trades
        
        results= {'page': page,
            'total_items':total_items,
            'total_pages': math.ceil(total_items/limit),
            'page_size':page_size,
            'data':orders}
    else:
        if currency==0 and bank==0:
            results_buy=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="buy").join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate.desc()).limit(limit).offset((page_buy-1)*limit).all()
            total_items_buy=db.query(models.Order).filter(models.Order.type=="buy").count()
            results_sell=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="sell").join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate).limit(limit).offset((page_sell-1)*limit).all()
            total_items_sell=db.query(models.Order).filter(models.Order.type=="sell").count()
        if currency!=0 and bank==0:
            results_buy=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="buy").filter(models.Order.currency_id==currency).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate.desc()).limit(limit).offset((page_buy-1)*limit).all()
            total_items_buy=db.query(models.Order).filter(models.Order.type=="buy").filter(models.Order.currency_id==currency).count()
            results_sell=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="sell").filter(models.Order.currency_id==currency).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate).limit(limit).offset((page_sell-1)*limit).all()
            total_items_sell=db.query(models.Order).filter(models.Order.type=="sell").filter(models.Order.currency_id==currency).count()
        if currency!=0 and bank != 0:
            results_buy=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="buy").filter(models.Order.currency_id==currency).filter(models.Order.bank_id==bank).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate.desc()).limit(limit).offset((page_buy-1)*limit).all()
            total_items_buy=db.query(models.Order).filter(models.Order.type=="buy").filter(models.Order.currency_id==currency).filter(models.Order.currency_id==currency).filter(models.Order.bank_id==bank).count()
            results_sell=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.type=="sell").filter(models.Order.currency_id==currency).filter(models.Order.bank_id==bank).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).order_by(models.Order.exchange_rate).limit(limit).offset((page_sell-1)*limit).all()
            total_items_sell=db.query(models.Order).filter(models.Order.currency_id==currency).filter(models.Order.currency_id==currency).filter(models.Order.type=="sell").filter(models.Order.bank_id==bank).count()
        if currency==0 and bank != 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail= "You must filter by currency first to filter by bank")
        orders_buy=[]
        for r in results_buy:
            order=r.Order
            order.availabe=r.available_balance
            orders_buy.append(order)
        orders_sell=[]
        for r in results_sell:
            order=r.Order
            order.availabe=r.available_balance
            orders_sell.append(order)
        page_size_buy=len(orders_buy)
        page_size_sell=len(orders_sell)
        for o in orders_buy:
            trades=db.query(models.Trade).filter(models.Trade.order_id==o.id).all()
            o.trades=trades
        for o in orders_sell:
            trades=db.query(models.Trade).filter(models.Trade.order_id==o.id).all()
            o.trades=trades
        results= {"buy":{
                'page': page_buy,
                'total_items':total_items_buy,
                'total_pages': math.ceil(total_items_buy/limit),
                'page_size':page_size_buy,
                'data':orders_buy},
                "sell":{
                'page': page_sell,
                'total_items':total_items_sell,
                'total_pages': math.ceil(total_items_sell/limit),
                'page_size':page_size_sell,
                'data':orders_sell
                }
            }
            

    return results

#Get all from user
@router.get("/{user_id}",status_code=status.HTTP_200_OK)
def get_orders(user_id: int,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user),
    page: int=1, limit:int=10):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    total_items=db.query(models.Order).filter(models.Order.owner_id==user_id).count()
    results=db.query(models.Order, (models.Order.amount-func.coalesce(func.sum(models.Trade.amount),0)).label('available_balance')).filter(models.Order.owner_id==user_id).join(models.Trade, models.Trade.order_id==models.Order.id, isouter=True).group_by(models.Order.id).limit(limit).offset((page-1)*limit).all()
    orders=[]
    for r in results:
        order=r.Order
        order.availabe=r.available_balance
        orders.append(order)
    page_size=len(orders)
    for o in orders:
        trades=db.query(models.Trade).filter(models.Trade.order_id==o.id).all()
        o.trades=trades
    
    return {'page': page,
        'total_items':total_items,
        'total_pages': math.ceil(total_items/limit),
        'page_size':page_size,
        'data':orders}

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
    new_trade=models.Trade(type=direction,currency_id=order.currency_id,owner_id=current_user.id,status='pending',fiat_amount=trade.amount*trade.exchange_rate,**trade.dict())
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade
    

