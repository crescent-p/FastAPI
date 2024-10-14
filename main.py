from fastapi import Body, FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Helfdsdfsdfworld'}
    
@app.get('/posts')
async def get_posts():
    return {"myposts": "hello tehre my biod"}

@app.post('/createposts')
async def create_post(payload: dict = Body(...)):
    return {"title": f"The message was { payload['message'] }"}