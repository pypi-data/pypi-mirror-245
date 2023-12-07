from typing import Any, Tuple

import pandas as pd

from .csv_config import CSVConfig
from .models import Sample


class DMASample(Sample):
    temp_range: Tuple[float, float] | None = None

    def model_post_init(
        self, __context: Any
    ) -> None:  # インスタンス生成後に実行される。csvから試料の大きさを取得する
        super().model_post_init(__context)
        if not self.temp_range:
            self.set_temp_range()
        return

    def set_temp_range(self) -> None:
        df = pd.read_csv(
            self.file_path,
            **CSVConfig(
                skiprows=[n for n in range(9)],
                nrows=1,
                usecols=[23, 31],
            ).to_dict(),
        )

        self.temp_range = df.values[0]
        return

    def get_result_df(self) -> pd.DataFrame:
        df = pd.read_csv(
            self.file_path,
            **CSVConfig().DMA().to_dict(),
        )
        return df
