from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    api_key: str

class UserUpdate(UserBase):
    api_key: str

class User(UserBase):
    id: int
    api_key: str

    class Config:
        orm_mode = True

class TweetBase(BaseModel):
    content: str

class TweetCreate(TweetBase):
    media_ids: Optional[List[int]] = []

class TweetUpdate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class Feed(BaseModel):
    result: bool
    tweets: List[Tweet]

    class Config:
        orm_mode = True

class OperationResult(BaseModel):
    result: bool

class MediaResponse(BaseModel):
    result: bool
    media_id: int

class UserProfileResponse(BaseModel):
    result: bool
    user: User

class UserResponse(BaseModel):
    result: bool
    user: User
