from fastapi import  FastAPI
from apps.routers import auth, posts, users, vote


##setting up the database. Creating the table and all
# models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can also use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(vote.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)




