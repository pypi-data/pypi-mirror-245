from enum import StrEnum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class encodingStr(StrEnum):
    shift_jis = "shift-jis"
    utf_8 = "utf-8"


class ColumnStrEnum(StrEnum):
    Voltage = "Voltage"
    Force = "Force /N"
    Stroke = "Stroke /mm"
    Wave_number = "Wave number /cm$^{-1}$"
    Absorbance = "Absorbance /a.u."
    Strain = "Strain $\epsilon$ /-"  # type: ignore
    Stress = "Stress $\sigma$ /MPa"  # type: ignore
    Temperature = "Temperature /℃"
    E1 = "$\it E'$ /Pa"  # type: ignore
    E2 = "$\it E''$ /Pa"  # type: ignore
    TanDelta = "tan $\delta$"  # type: ignore
    RamanShift = "Raman Shift /cm$^{-1}$"
    Intensity = "Intensity /a.u."


col = ColumnStrEnum


class CSVConfig(BaseModel):
    encoding: encodingStr = encodingStr.shift_jis
    sep: str = ","
    header: Optional[int] = None
    names: Optional[List[str]] = None
    usecols: Union[List[int], List[str], None] = None
    dtype: Optional[Dict[str, type]] = None
    skiprows: Optional[List[int]] = None  # 冒頭の行を読み飛ばす動作は許可しない
    skipfooter: int = 0
    engine: str = "python"
    nrows: Optional[int] = None

    def to_dict(self) -> Dict:
        return self.model_dump()

    def Instron(self) -> "CSVConfig":
        self.header = 51
        self.skipfooter = 3
        self.names = ["EndHeader", "日時(μs)", col.Voltage]
        self.usecols = [col.Voltage]
        self.dtype = {col.Voltage: float}
        return self

    def AGIS(self) -> "CSVConfig":
        self.header = 19
        self.names = ["sec", col.Force, col.Stroke]
        self.usecols = [col.Force, col.Stroke]
        self.dtype = {col.Force: float, col.Stroke: float}
        return self

    def DMA(self) -> "CSVConfig":
        self.header = 27
        self.skiprows = [28]
        self.names = [
            "TOTAL",
            "BL",
            "No",
            col.Temperature,
            "FREQ.",
            "ω",
            col.E1,
            col.E2,
            "E*",
            col.TanDelta,
            "η'",
            "η''",
            "η * ",
            "Time",
            "DISP",
            "DISP.1",
            "FORCE",
            "LOAD",
            "C.D",
            "PHASE",
            "応力",
            "S.STRESS",
            "N.STRESS",
            "REVL",
            "HUMIDITY ",
            "F/L",
            "Ld",
            "TempB",
            "TempC",
            "J*",
            "J'",
            "J''",
            " W ",
            " TempC",
            "*",
        ]
        self.usecols = [
            col.Temperature,
            col.E1,
            col.E2,
            col.TanDelta,
        ]
        self.dtype = {
            col.Temperature: float,
            col.E1: float,
            col.E2: float,
            col.TanDelta: float,
        }
        return self

    def IR_NICOLET(self) -> "CSVConfig":
        self.names = [col.Wave_number, col.Absorbance]
        self.usecols = [col.Wave_number, col.Absorbance]
        self.dtype = {col.Wave_number: float, col.Absorbance: float}
        return self

    def Raman(self) -> "CSVConfig":
        self.sep = "\t"
        self.names = [col.RamanShift, "1", col.Intensity]
        self.usecols = [col.RamanShift, col.Intensity]
        self.dtype = {col.RamanShift: float, col.Intensity: float}
        return self
