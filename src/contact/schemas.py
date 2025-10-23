from pydantic import BaseModel, EmailStr


class EmailModel(BaseModel):
    name: str
    message: str
    address: EmailStr
