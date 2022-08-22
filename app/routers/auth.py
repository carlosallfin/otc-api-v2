from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from requests import Session
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router=APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends() ,db: Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    logged=False
    if not user:
        detail='User does not exist'
        logged=False

    if user:
        if user.active==False:
            detail= 'User is inactive'
            logged=False
        else:
            if not utils.verify(user_credentials.password, user.password):
                detail= 'Invalid password'
                logged=False

            else:
                logged=True
                access_token= oauth2.create_access_token(data={"user_id": user.id})
                detail='Success'
                token_type='Bearer'
                current_user={
                    "id":user.id,
                    "name":user.name,
                    "email":user.email,
                    "phone":user.phone,
                    "role_id":user.role_id,
                    "active":user.active
                }

    if logged==False:
        access_token=''
        token_type=''
        current_user={}
    
    return {'logged':logged, 'detail':detail,"access_token":access_token, "token_type":token_type, "user_data":current_user}
