from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from config import Config

engine = create_engine(Config.DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as db:
        yield db


db_dep = Annotated[Session, Depends(get_db)]
