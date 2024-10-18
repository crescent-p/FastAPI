import time
from fastapi import  FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from apps.routers import auth, posts, users
from . import models
from .database import engine


#setting up the database. Creating the table and all
models.Base.metadata.create_all(bind=engine)

#connecting to the database.
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

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



