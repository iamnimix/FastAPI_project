from pydantic import BaseModel, Field


class Comments(BaseModel):
    description: str
    post_id: int
