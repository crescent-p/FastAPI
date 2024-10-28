from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.oauth import get_current_user
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/author", tags=['Author'])


@router.post('/', response_model=schemas.AuthorOut)
async def create_author(author: schemas.Author,db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    conflict = db.query(models.Author).where(models.Author.name == author.name).first()

    if conflict:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A author with same name already exists!")
    
    new_author = models.Author(**author.model_dump())
    
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    
    return new_author

@router.get('/{id}', response_model=schemas.AuthorOut)
async def get_author(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    author = db.query(models.Author).where(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The Author with id doesn't exist!")
    return author
