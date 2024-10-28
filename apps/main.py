from fastapi import  FastAPI, status
from apps.routers import auth, author, book_issues, books, students, users


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

@app.get('/', status_code=status.HTTP_200_OK)
async def test():
    return {"message": "all good boi!!"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(books.router)
app.include_router(book_issues.router)
app.include_router(author.router)




