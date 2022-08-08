from sqlite3 import apilevel
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models,schemas,utils,oauth2
from database import get_db
from sqlalchemy import func

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

#ORM create user
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    #hash password - user.password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#ORM get user
@router.get("/{id}", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOutColl)
# @router.get("/{id}", status_code=status.HTTP_201_CREATED)
def get_user(id: int ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.id != id or current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    
    col=db.query(func.sum(models.Collateral.amount)).filter(models.Collateral.owner_id==id).filter(models.Collateral.status=='verified').first()[0]
    if not col:
        user.balance=0
    else: 
        user.balance=round(col,2)

    # for c in collat:
    #     print(c.amount)
    # results=db.query(models.User, func.sum(models.Collateral.owner_id))
    # print(results)
    return user

@router.get("/test/{id}", status_code=status.HTTP_201_CREATED)
# @router.get("/{id}", status_code=status.HTTP_201_CREATED)
def get_user(id: int ,db: Session = Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    if current_user.id != id or current_user.role_id != 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    results=db.query(models.Collateral.owner_id,models.User.email,models.User.name,func.sum(models.Collateral.amount)).join(models.User, models.User.id==models.Collateral.owner_id, isouter=True).group_by(models.Collateral.owner_id,models.User.email,models.User.name)
    print(results)
    # col=db.query(func.sum(models.Collateral.amount)).filter(models.Collateral.owner_id==id).filter(models.Collateral.status=='verified').first()[0]
    # if not col:
    #     user.balance=0
    # else: 
    #     user.balance=round(col,2)

    # for c in collat:
    #     print(c.amount)
    # results=db.query(models.User, func.sum(models.Collateral.owner_id))
    # print(results)
    # return results
