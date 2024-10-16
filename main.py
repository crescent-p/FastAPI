from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title 1", "body": "content1", "id": 1}, {"title": "title 2", "body": "content2", "id": 2}]

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post('/createposts')
async def create_post(posts: Posts):
    my_post = posts.model_dump()
    my_post['id'] = randrange(0, 100000)
    my_posts.append(my_post)
    return {"body": my_post}

@app.get('/')
async def root():
    return {'message': my_posts}
    
@app.get('/posts')
async def get_posts():
    return {"myposts": "hello tehre my biod"}

def find_post(id):
    for i in my_posts:
        if(i['id'] == id):
            return i
    return None

@app.get('/posts/{id}')
async def get_post(id: int):
    return {'data': find_post(int(id))}