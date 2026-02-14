from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

# Магия Pydantic V2: хелпер, который конвертирует ObjectId в строку для JSON
PyObjectId = Annotated[str, BeforeValidator(str)]


# --- АВТОРЫ ---
class AuthorBase(BaseModel):
    name: str
    # Список ID книг, написанных автором (Связь Многие-ко-многим)
    book_ids: list[PyObjectId] = []


class AuthorDB(AuthorBase):
    id: PyObjectId | None = Field(alias="_id", default=None)
    model_config = ConfigDict(populate_by_name=True)


# --- КНИГИ ---
class BookBase(BaseModel):
    title: str
    description: str
    # Список ID авторов (Связь Многие-ко-многим)
    author_ids: list[PyObjectId] = []


class BookDB(BookBase):
    id: PyObjectId | None = Field(alias="_id", default=None)
    model_config = ConfigDict(populate_by_name=True)
