from pydantic import BaseModel, Field, ConfigDict


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=40)
    variant: int


class AuthResponse(BaseModel):
    id: int
    name: str
    variant_number: int

    model_config = ConfigDict(from_attributes=True)