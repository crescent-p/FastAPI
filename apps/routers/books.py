from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/books", tags=['books'])

@router.post('/', response_model=schemas.BooksOut, status_code=status.HTTP_201_CREATED)
async def add_book(book: schemas.Books, db: Session = Depends(get_db)):

    new_book = models.Books(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.get('/{id}', response_model=schemas.BooksOut, status_code=status.HTTP_302_FOUND)
async def get_book_by_id(id:int, db: Session = Depends(get_db)):
    
    query_res = db.query(models.Books).where(models.Books.book_code == id).first()
    if not query_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id: {id} doesn't exist!")
    return query_res

@router.get('/',response_model=List[schemas.BooksOut], status_code=status.HTTP_302_FOUND)
async def get_all_books(db: Session = Depends(get_db), author_id: Optional[int] = 1):
    
    query_res = db.query(models.Books).all()
    if not query_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books currently exist in library!")
    return query_res

@router.delete('/{id}', response_model=schemas.BooksOut, status_code=status.HTTP_200_OK)
async def delete_book_by_id(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Books).where(models.Books.book_code == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The book with id: {id} doesn't exist!")

    deleted_book = query.first()
    if deleted_book:
        query.delete()
        db.commit()

    return deleted_book