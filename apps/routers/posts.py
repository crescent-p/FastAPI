from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from apps import schemas
from apps.oauth import get_current_user
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['posts'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(posts: schemas.PostBase, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    new_post = models.Post(**posts.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).where(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id doesn't exist!")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    # delete_post = cursor.fetchone()
    query = db.query(models.Post).where(models.Post.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id couldn't be found!")
    query.delete()
    db.commit()
    return delete_post
    
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id: int, post: PostBase, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (str(post.title), str(post.content), str(post.published), str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).where(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The said id {id} doesn't exist")
    else:
        query.update(post.model_dump())
        db.commit()
        return db.query(models.Post).where(models.Post.id == id).first()

