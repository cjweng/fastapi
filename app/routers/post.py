from email.policy import default
from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),
                    user_id: int = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    #cursor.execute("""select * from posts""")
    #posts = cursor.fetchall()
    print(limit)
    print(skip)
    print(search)
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(
                           models.Vote,
                           models.Vote.post_id == models.Post.id,
                           isouter=True).group_by(models.Post.id).filter(
                               models.Post.title.contains(search)).limit(
                                   limit).offset(skip).all()
    print(results)
    return results


@router.get("/{id}", response_model=schemas.PostOut)
async def get_posts(id: int,
                    response: Response,
                    db: Session = Depends(get_db),
                    user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    #cursor.execute("""SELECT * from posts where id = %s""", [str(id)])
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(
                           models.Vote,
                           models.Vote.post_id == models.Post.id,
                           isouter=True).group_by(models.Post.id).filter(
                               models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 user: models.User = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user.email)
    new_post = models.Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,
                 db: Session = Depends(get_db),
                 user: models.User = Depends(oauth2.get_current_user)):

    print(id)
    #cursor.execute("""delete from posts where id = %s returning *""", [str(id)])
    #post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        post.delete(synchronize_session=False)
        db.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int,
                 post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 user: models.User = Depends(oauth2.get_current_user)):
    post_dict = post.dict()

    # cursor.execute(
    #     """UPDATE posts set title = %s, content = %s, published = %s where id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post_query.first().owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return (post_query.first())
