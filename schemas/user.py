from pydantic import BaseModel, EmailStr, UUID4


class CreateUserData(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class RoleAssignSchema(BaseModel):
    role_id: int


class UserDetails(BaseModel):
    id: UUID4
    first_name: str = None
    last_name: str = None
    email: EmailStr
    is_active: bool
    is_superuser: bool
