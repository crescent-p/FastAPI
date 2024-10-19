from fastapi import  FastAPI
from apps.routers import auth, posts, users
from . import models
from .database import engine


#setting up the database. Creating the table and all
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



