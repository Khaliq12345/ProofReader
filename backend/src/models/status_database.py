from sqlmodel import Field, SQLModel
from src.core import config
from typing import Optional


class Status(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    folder_name: str
    status: Optional[str] = None


def create_db_and_tables():
    SQLModel.metadata.create_all(config.engine)
