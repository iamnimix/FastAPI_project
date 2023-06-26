from pydantic import BaseModel, Field, validator


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterNewUser(BaseModel):
    fullname: str
    username: str
    email: str = Field(regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$")
    password: str = Field(regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")
    password_confirmation: str

    @validator('password_confirmation')
    @classmethod
    def check_password_confirmation(cls, value, values):
        if values["password"] != value:
            raise ValueError('Password Confirmation must match password')

        return value

