from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: Optional[datetime]
    user_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

class Students(BaseModel):
    name: str
    address: str
    status: Optional[conint(ge=0, le=1)] #0 means temporary 1 means Permanent

class StudentsOut(BaseModel):
    id_no: int
    name: str
    address: str
    status: str
    date_of_issue: datetime
    date_of_expiry: datetime

    class Config:
        from_attributes = True
        
class Books(BaseModel):
    book_name: str
    author_id: int
    price: float
    rack_no: int
    no_of_books: Optional[int] = 1

class BooksOut(Books):
    book_code: int
    date_of_arrival: datetime

class Issues(BaseModel):
    student_id : int
    book_id: int

class IssuesOut(Issues):
    issue_date: datetime
    due_date: datetime

class Author(BaseModel):
    name: str
    age: int 

class AuthorOut(Author):
    id: int

class StudentIssues(BaseModel):
    student: StudentsOut
    issue: IssuesOut

    class Config:
        from_attributes = True