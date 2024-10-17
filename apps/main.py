from random import randrange
import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host="localhost", database='fastapi',user='crescent', 
                                password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected Succesfully")
        break
    except Exception as error:
        print(str(error))
        time.sleep(2)


app = FastAPI()

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



@app.get('/')
async def root():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
async def create_post(posts: Posts):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (posts.title, posts.content, posts.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"body": new_post}


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id doesn't exist!")
    return {"result": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
   cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
   delete_post = cursor.fetchone()
   if not delete_post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The given id couldn't be found!")
   conn.commit()
   return delete_post
    
@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Posts):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (str(post.title), str(post.content), str(post.published), str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The said id {id} doesn't exist")
    else:
        return {"updated_post": updated_post}
