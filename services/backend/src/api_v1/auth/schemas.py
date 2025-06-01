from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=40)
    variant: int


class AuthResponse(BaseModel):
    id: int
    name: str
    variant_number: int