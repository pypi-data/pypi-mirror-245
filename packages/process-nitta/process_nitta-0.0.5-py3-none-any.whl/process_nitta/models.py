from pydantic import BaseModel


class Base(BaseModel):
    file_path: str
    name: str


class Sample(Base):
    width: float
    length: float
    thickness: float
