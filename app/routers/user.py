from fastapi import Depends, FastAPI, Response, HTTPException, status, APIRouter

from .. import models
from ..database import get_db
from .. import schemas
from .. import utils
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
