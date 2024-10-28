from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.oauth import get_current_user
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/students", tags=['students'])



@router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model=List[schemas.StudentsOut])
async def get_all_students(db: Session = Depends(get_db), limit: int = 10):
    query_res = db.query(models.Students).limit(limit=limit).where(models.Students.id_no == id).first()
    return query_res


@router.get('/', status_code=status.HTTP_302_FOUND, response_model=List[schemas.StudentsOut])
async def get_all_students(db: Session = Depends(get_db), limit: int = 10):
    query_res = db.query(models.Students).limit(limit=limit).all()
    return query_res


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StudentsOut)
async def create_student(user: schemas.Students, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):

    if db.query(models.Students).where(models.Students.name == user.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This username is taken!")

    if user.status:
        if user.status == 1:
            user.status = "Permanent"
        else:
            user.status = "Temporary"
    new_user = models.Students(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

