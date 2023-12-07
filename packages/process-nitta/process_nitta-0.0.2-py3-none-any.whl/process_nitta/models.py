from typing import Optional

from pydantic import BaseModel


class Base(BaseModel):
    file_path: str
    name: str


class Sample(Base):
    width: Optional[float]
    length: Optional[float]
    thickness: Optional[float]
