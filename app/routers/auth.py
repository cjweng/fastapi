from fastapi import Depends, FastAPI, Response, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.database import get_db
from .. import database, schemas, models, utils, oauth2
router = APIRouter(tags=['Autthentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



