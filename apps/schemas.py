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
    
