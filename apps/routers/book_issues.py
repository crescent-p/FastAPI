from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from apps import schemas
from .. import models
from ..database import get_db

router = APIRouter(prefix="/bookissues", tags=["BookIssues"])
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.IssuesOut])
async def get_all_issues(db: Session = Depends(get_db)):
    issues = (
        db.query(models.Issue, models.Students, models.Books)
        .join(models.Students, models.Issue.student_id == models.Students.id_no)
        .join(models.Books, models.Issue.book_id == models.Books.book_code)
        .all()
    )
    
    # Format the issues to match the IssuesOut schema
    formatted_issues = [
        {
            "student_id": issue.student_id,      # Add student_id directly from Issue model
            "book_id": issue.book_id,            # Add book_id directly from Issue model
            "issue_date": issue.issue_date,
            "due_date": issue.due_date,
            "student": {
                "id_no": student.id_no,
                "name": student.name,
                "address": student.address,
                "email": student.email,
                "phone_number": student.phone_number,
                "status": student.status,
                "date_of_issue": student.date_of_issue,
                "date_of_expiry": student.date_of_expiry
            },
            "book": {
                "book_name": book.book_name,
                "book_code": book.book_code,
                "author_id": book.author_id,
                "price": book.price,
                "rack_no": book.rack_no,
                "no_of_books": book.no_of_books,
                "date_of_arrival": book.date_of_arrival
            }
        }
        for issue, student, book in issues  # Unpacking each tuple into variables
    ]
    
    return formatted_issues


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

    student_book = (
        db.query(models.Issue)
        .join(models.Students, models.Issue.student_id == models.Students.id_no)  # Join Issue with Students on student_id
        .join(models.Books, models.Issue.book_id == models.Books.book_code)  # Join Issue with Books on book_id
        .with_entities(
            models.Issue.issue_date,
            models.Issue.due_date,
            models.Students.name.label("student_name"),
            models.Students.id_no.label("student_id"),
            models.Books.book_name.label("book_name"),
            models.Books.book_code.label("book_id")
        ).filter(models.Issue.book_id == issue.book_id & models.Issue.student_id == issue.student_id)
        .first()
    )
    
    # Format the issues to match the IssuesOut schema
    formatted_issues = {
            "id": student_book.id,
            "issue_date": student_book.issue_date,
            "due_date": student_book.due_date,
            "student": {"name": student_book.student_name, "id_no": student_book.student_id},
            "book": {"book_name": student_book.book_name, "book_code": student_book.book_id}
        }

    return formatted_issues

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_issue( student_id: int, book_id: int, db: Session = Depends(get_db)):
    from sqlalchemy import and_
    issue = db.query(models.Issue).filter(and_(models.Issue.student_id == student_id, models.Issue.book_id == book_id)).first()
    
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    
    book = db.query(models.Books).filter(models.Books.book_code == issue.book_id).first()
    
    if book:
        book.no_of_books += 1
        db.commit()
        db.refresh(book)
    
    db.delete(issue)
    db.commit()
    