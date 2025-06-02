from pydantic import BaseModel, ConfigDict, Field


class ChatBaseSchema(BaseModel):
    subject: str


class ChatCreateSchema(ChatBaseSchema):
    subject: str = Field(...,max_length=40)


class ChatUpdateSchema(ChatCreateSchema):
    subject: str | None = None


class ChatSchema(ChatBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
