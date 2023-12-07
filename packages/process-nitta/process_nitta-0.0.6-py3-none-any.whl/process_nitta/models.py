from pydantic import BaseModel


class Base(BaseModel):
    file_path: str
    name: str


class Sample(Base):
    width_mm: float
    length_mm: float
    thickness_μm: float
