from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from apps import schemas
from .. import models
from ..database import get_db

router = APIRouter(prefix="/request", tags=["Request"])

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.RequestOut])
async def get_all_requests(db: Session = Depends(get_db)):
    issues = db.query(models.Request).all()
    return issues


@router.post('/', response_model=schemas.RequestOut, status_code=status.HTTP_201_CREATED)
async def create_a_request(issue: schemas.Request ,db: Session = Depends(get_db)):

    query = db.query(models.Request).where(models.Request.ISBN == issue.ISBN).first()

    if query:
        raise HTTPException(detail="A request for this book already exists", status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    new_request = models.Request(**issue.model_dump())

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.delete('/{request_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(ISBN: str, db: Session = Depends(get_db)):
    request_to_delete = db.query(models.Request).filter(models.Request.ISBN == ISBN).first()

    if not request_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")

    db.delete(request_to_delete)
    db.commit()

    return {"detail": "Request deleted successfully"}