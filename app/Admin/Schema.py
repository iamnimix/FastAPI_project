from pydantic import BaseModel, Field


class NewPost(BaseModel):
    # image: str
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    created_date: str


class PostID(BaseModel):
    post_id: int
    # created_date: str