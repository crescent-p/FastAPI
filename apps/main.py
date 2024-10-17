from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

def find_post(id):
    for i in my_posts:
        if(i['id'] == id):
            return i
    return None

def find_index_post(id):
    for index, value in enumerate(my_posts):
        if(int(value['id']) == int(id)):
            return index
    return -1

my_posts = [{"title": "title 1", "body": "content1", "id": 1}, {"title": "title 2", "body": "content2", "id": 2}]

class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
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


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    post = find_post(int(id))
    if(not post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    # if(not post):
    #     response.status_code = status.HTTP_404_NOT_FOUND
    return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    index = find_index_post(id)
    if(index == -1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        my_posts.pop(index)
        return {"message": "succesffully deletd"}
    
@app.put('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_post(id: int, post: Posts):
    index = find_index_post(id)
    if(index == -1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The said id {id} doesn't exist")
    else:
        post_dic = post.model_dump()
        post_dic['id'] = id
        my_posts[index] = post_dic
        return {"Message": "the message is updated"}
