from typing import Any

import pandas as pd

from .csv_config import ColumnStrEnum as col
from .csv_config import CSVConfig
from .models import Sample


class AGISSample(Sample):
    calibration_coefficient: float = 0.84  # 2023/1/02時点
    width_mm: float = 0
    length_mm: float = 0
    thickness_μm: float = 0

    def model_post_init(
        self, __context: Any
    ) -> None:  # インスタンス生成後に実行される。csvから試料の大きさを取得する
        super().model_post_init(__context)
        if not all([self.width_mm, self.length_mm, self.thickness_μm]):
            self.set_sample_size()
        return

    def set_sample_size(self) -> None:
        size_df = pd.read_csv(
            self.file_path,
            **CSVConfig(
                skiprows=[n for n in range(10)],
                nrows=1,
                usecols=[1, 2, 3],
                dtype={"1": float, "2": float, "3": float},
            ).to_dict(),
        )

        thickness_mm, self.width_mm, self.length_mm = size_df.values[0]
        self.thickness_μm = thickness_mm * 1000
        return

    def trim_df(self, df: pd.DataFrame, mean_range=10) -> pd.DataFrame:
        df = df.copy()
        roll = pd.DataFrame(df[col.Force].rolling(window=mean_range).mean().diff())

        start = (
            int(roll[col.Force][mean_range : mean_range * 2].idxmax()) - mean_range + 1
        )  # 傾きが最大のところを探す

        result = df[start:].reset_index(drop=True)
        result[col.Stroke] = result[col.Stroke] - result[col.Stroke][0]
        result[col.Force] = result[col.Force] - result[col.Force][0]
        return result

    def calc_stress_strain_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        area_mm2 = self.width_mm * self.thickness_μm / 1000

        stress_Mpa = self.calibration_coefficient * df[col.Force] / area_mm2
        strain = df[col.Stroke] / self.length_mm

        return pd.DataFrame(
            {col.Strain: strain, col.Stress: stress_Mpa},
        )

    def get_stress_strain_df(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path, **CSVConfig().AGIS().to_dict())
        return self.calc_stress_strain_df(self.trim_df(df))
