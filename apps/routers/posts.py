from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from apps import schemas
from apps.oauth import get_current_user
from apps.schemas import PostBase
from .. import models
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['posts'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(posts: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    new_post = models.Post(**posts.model_dump())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/', response_model=List[schemas.PostOut])
async def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    query = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Votes, models.Votes.posts_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    print(query)
    return query
    # return db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip)

@router.get('/{id}', response_model=schemas.PostOut)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).where(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Votes, models.Votes.posts_id == models.Post.id, isouter=True).where(models.Post.id == id).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id doesn't exist!")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    # delete_post = cursor.fetchone()
    query = db.query(models.Post).where(models.Post.id == id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id couldn't be found!")
    if query.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This post was not created by you.")
    query.delete()
    db.commit()
    return delete_post
    
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(id: int, post: PostBase, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                (str(post.title), str(post.content), str(post.published), str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    query = db.query(models.Post).where(models.Post.id == id)

    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The said id {id} doesn't exist")
    else:
        if query.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This post was not created by you.")
        query.update(post.model_dump())
        db.commit()
        return db.query(models.Post).where(models.Post.id == id).first()

