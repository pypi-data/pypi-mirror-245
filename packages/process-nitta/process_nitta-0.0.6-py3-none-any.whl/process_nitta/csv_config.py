from enum import StrEnum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class encodingStr(StrEnum):
    shift_jis = "shift-jis"
    utf_8 = "utf-8"


class CSVConfig(BaseModel):
    encoding: encodingStr = encodingStr.shift_jis
    sep: str = ","
    header: Optional[int] = None
    usecols: Union[List[int], List[str], None] = None
    names: Optional[List[str]] = None
    dtype: Optional[Dict[str, type]] = None
    skiprows: Optional[List[int]] = None  # 冒頭の行を読み飛ばす動作は許可しない
    skipfooter: int = 0
    engine: str = "python"

    def to_dict(self) -> Dict:
        return self.model_dump()

    def Instron(self) -> "CSVConfig":
        self.header = 51
        self.skipfooter = 3
        self.usecols = ["Voltage"]
        self.names = ["EndHeader", "日時(μs)", "Voltage"]
        self.dtype = {"Voltage": float}
        return self

    def AGIS(self) -> "CSVConfig":
        self.header = 19
        self.usecols = ["Force", "Stroke"]
        self.names = ["Force", "Stroke"]
        self.dtype = {"Force": float, "Stroke": float}
        return self

    def DMA(self) -> "CSVConfig":
        self.header = 27
        self.skiprows = [28]
        self.usecols = ["TEMP", "E'", "E ''", "tanδ"]
        self.dtype = {"E'": float, "E''": float, "tanδ": float}
        return self

    def IR(self) -> "CSVConfig":
        self.header = None
        self.usecols = ["Wave number /cm$^{-1}$", "Absorbance /a.u."]
        self.names = ["Wave number /cm$^{-1}$", "Absorbance /a.u."]
        self.dtype = {"Wave number /cm$^{-1}$": float, "Absorbance /a.u.": float}
        return self
