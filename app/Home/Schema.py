from pydantic import BaseModel, Field


class Messages(BaseModel):
    created_by: str = Field(min_length=3)
    email: str = Field(regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")
    description: str = Field(min_length=1)
