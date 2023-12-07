import pandas as pd

from .csv_config import CSVConfig
from .models import Sample


class InstronSample(Sample):
    speed_mm_per_min: float
    freq_Hz: float
    load_cell_max_N: int = 100
    load_range: int = 1
    max_Voltage: float = 10

    def trim_instron_df(self, df: pd.DataFrame, meat_range: int = 100) -> pd.Series:
        df = df.copy()
        roll = pd.DataFrame(df["Voltage"].rolling(window=meat_range).mean().diff())

        start = (
            int(roll["Voltage"][0 : meat_range * 10].idxmax()) - meat_range + 1
        )  # 傾きが最大のところを探す
        end = int(roll["Voltage"].idxmin()) + 10

        result = df["Voltage"][start:end].reset_index(drop=True)

        return result - result[0]  # 初期値を0にする

    def calc_stress_strain_df(self, sr: pd.Series) -> pd.DataFrame:
        sr = sr.copy()
        area_mm2 = self.width_mm * self.thickness_μm / 1000
        speed_mm_per_sec = self.speed_mm_per_min / 60

        stress_Mpa = (
            self.load_cell_max_N / (self.load_range * self.max_Voltage) / area_mm2 * sr
        )
        strain = speed_mm_per_sec * self.freq_Hz * sr.index / self.length_mm

        strain_label = "Strain"  # type: ignore
        stress_label = "Stress_MPa"  # type: ignore
        return pd.DataFrame(
            {strain_label: strain, stress_label: stress_Mpa}, index=sr.index
        )

    def get_stress_strain_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path, **CSVConfig().Instron().to_dict())
        return self.calc_stress_strain_df(self.trim_instron_df(df))
