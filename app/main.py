from random import randrange
from turtle import pos
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

import psycopg2
from psycopg2.extras import RealDictCursor

from  sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models
from .database import get_db
from . import schemas
from . import utils
models.Base.metadata.create_all(bind=engine)
from .routers import post, user, auth, vote

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# try:
#     conn = psycopg2.connect(host='localhost',
#                             database='fastapi',
#                             user='postgres',
#                             password='jia1130',
#                             cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Connect db successful")
# except Exception as e:
#     print(e)



