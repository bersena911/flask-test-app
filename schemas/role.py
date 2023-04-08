from pydantic import BaseModel


class CreateRole(BaseModel):
    name: str


class Role(BaseModel):
    id: int
    name: str
