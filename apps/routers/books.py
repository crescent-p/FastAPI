from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/books", tags=['books'])

@router.post('/', response_model=schemas.Books, status_code=status.HTTP_201_CREATED)
async def add_book(book: schemas.Books, db: Session = Depends(get_db)):

    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()

    if not author:
        raise HTTPException(detail="The provided author doesnt exist", status_code=status.HTTP_404_NOT_FOUND)

    new_book = models.Books(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.get('/{id}', response_model=schemas.BooksOut, status_code=status.HTTP_302_FOUND)
async def get_book_by_id(id:int, db: Session = Depends(get_db)):
    
    query_res = db.query(models.Books, models.Author).join(models.Author, models.Author.id == models.Books.author_id).where(models.Books.book_code == id).first()
    
    if not query_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The book with id: {id} doesn't exist!")
    

    book = query_res[0]
    author = query_res[1]

    final_res = {
        "price": book.price,
        "rack_no": book.rack_no,
        "author_id": book.author_id,
        "book_name": book.book_name,
        "book_code": book.book_code,
        "author_name": author.name,  # Assuming 'name' is the field for the author's name in the Author model
        "book_code": book.book_code,  # Assuming 'book_code' is available in Books model
        "date_of_arrival": book.date_of_arrival  # Assuming 'date_of_arrival' exists in the Books model
    }

    return final_res






@router.get('/', response_model=List[schemas.BooksOut], status_code=status.HTTP_302_FOUND)
async def get_all_books(db: Session = Depends(get_db), book_name: str = ""):
    
    query_res = db.query(models.Books, models.Author).join(models.Author, models.Author.id == models.Books.author_id).filter(func.lower(models.Books.book_name).contains(func.lower(book_name))).all()
    
    if not query_res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No books currently exist in library!")
    
    final_res = [{
        "price": book.price,
        "rack_no": book.rack_no,
        "author_id": book.author_id,
        "book_name": book.book_name,
        "book_code": book.book_code,
        "author_name": author.name,  # Assuming 'name' is the field for the author's name in the Author model
        "book_code": book.book_code,  # Assuming 'book_code' is available in Books model
        "date_of_arrival": book.date_of_arrival  # Assuming 'date_of_arrival' exists in the Books model
    } for book, author in query_res]

    return final_res

@router.delete('/{id}', response_model=schemas.Books, status_code=status.HTTP_200_OK)
async def delete_book_by_id(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Books).where(models.Books.book_code == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The book with id: {id} doesn't exist!")

    deleted_book = query.first()
    if deleted_book:
        query.delete()
        db.commit()

    return deleted_book