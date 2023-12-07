import os

from pydantic import BaseModel


class Base(BaseModel):
    file_path: str
    name: str = ""

    def model_post_init(self, __context: object) -> None:
        if not self.name:
            base_name = os.path.basename(self.file_path)
            self.name = os.path.splitext(base_name)[0]
        return


class Sample(Base):
    width_mm: float
    length_mm: float
    thickness_μm: float
