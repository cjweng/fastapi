from email.policy import default
from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,
         db: Session = Depends(get_db),
         user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id==user.id)
    found_vote = vote_query.first()
    if (vote.dir ==1) :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        new_vote = models.Vote(post_id = vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"msg": "successfully add vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "successfully delete vote"}


