from pydantic import BaseModel, EmailStr, UUID4


class UserDetails(BaseModel):
    id: UUID4
    first_name: str = None
    last_name: str = None
    email: EmailStr
    is_active: bool
    is_superuser: bool
