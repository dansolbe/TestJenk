from pydantic import BaseModel, Field


# User AUTH/NOAUTH
class User(BaseModel):
    login: str
    display_name: str


class DiskInfoResponse(BaseModel):
    user: User


class DI_ErrorResponse(BaseModel):
    error: str
    description: str
    message: str


# Trash response
class TrashItem(BaseModel):
    path: str
    name: str


class EmbeddedTrash(BaseModel):
    items: list[TrashItem]


class TrashResponse(BaseModel):
    embedded: EmbeddedTrash = Field(alias="_embedded")


# Folder response
class CreatedResponse(BaseModel):
    method: str
    href: str
    templated: bool
