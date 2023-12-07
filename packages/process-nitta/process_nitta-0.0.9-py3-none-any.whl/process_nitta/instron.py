import pandas as pd

from .csv_config import ColumnStrEnum as col
from .csv_config import CSVConfig
from .models import Sample


class InstronSample(Sample):
    speed_mm_per_min: float
    freq_Hz: float = 0.05
    load_cell_max_N: int = 100
    load_cell_calibration_coef: float = 1
    max_Voltage: float = 10
    mean_range: int = 100

    def trim_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        roll = pd.DataFrame(
            df[col.Voltage].rolling(window=self.mean_range).mean().diff()
        )

        start = (
            int(roll[col.Voltage][self.mean_range : self.mean_range * 2].idxmax())
            - self.mean_range
            + 1
        )  # 傾きが最大のところを探す
        end = int(roll[col.Voltage].idxmin()) + 10

        result = df[start:end].reset_index(drop=True)
        result[col.Voltage] = (
            result[col.Voltage] - result[col.Voltage][0]
        )  # 初期値を0にする

        return result

    def calc_stress_strain_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        area_mm2 = self.width_mm * self.thickness_μm / 1000
        speed_mm_per_sec = self.speed_mm_per_min / 60

        stress_Mpa = (
            self.load_cell_max_N
            / (self.load_cell_calibration_coef * self.max_Voltage)
            / area_mm2
            * df[col.Voltage]
        )
        strain = speed_mm_per_sec * self.freq_Hz * df.index / self.length_mm

        return pd.DataFrame(
            {col.Strain: strain, col.Stress: stress_Mpa},
        )

    def get_stress_strain_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path, **CSVConfig().Instron().to_dict())
        return self.calc_stress_strain_df(self.trim_df(df))
