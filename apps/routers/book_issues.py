from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from apps import schemas
from .. import models
from ..database import get_db

router = APIRouter(prefix="/bookissues", tags=["BookIssues"])

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.IssuesOut])
async def get_all_issues(db: Session = Depends(get_db)):
    issues = db.query(models.Issue).all()
    return issues


@router.post('/', response_model=schemas.IssuesOut, status_code=status.HTTP_201_CREATED)
async def create_an_issue(issue: schemas.Issues ,db: Session = Depends(get_db)):
    
    #check for that user and book, if any not present raise exception
    #after this check no of books. if no of books == 0 raise unavailable
    student = db.query(models.Students).where(models.Students.id_no == issue.student_id).first()
    if not student: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="That user doesn't exist")
    
    book = db.query(models.Books).where(models.Books.book_code == issue.book_id).first()
    if not book: 
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="That book doesn't exist")
    
    studentBookPair = db.query(models.Issue).where((models.Issue.book_id == issue.book_id) & (models.Issue.student_id == issue.student_id)).first()

    if studentBookPair:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This student already own a copy of this book.")

    book_count = book.no_of_books
    
    if book_count <= 0:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There are no more copies of the book available at this time.")
    book.no_of_books = book.no_of_books - 1
    db.commit()
    db.refresh(book)

    new_issue = models.Issue(**issue.model_dump())

    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)

    return new_issue