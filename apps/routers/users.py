import time
from typing import List, Optional
from fastapi import APIRouter, Body, Depends, FastAPI, Response, status, HTTPException
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from apps import schemas
from apps.schemas import UserCreate
from .. import models
from ..database import  get_db

from apps import utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: UserCreate,db: Session = Depends(get_db)):
    
    if(db.query(models.Admin).where(models.Admin.email==user.email).first()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A email with same address exists")
    
    user.password = utils.hash(user.password)
    new_user = models.Admin(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model= schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Admin).where(models.Admin.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id couldn't be found")
    
    return user