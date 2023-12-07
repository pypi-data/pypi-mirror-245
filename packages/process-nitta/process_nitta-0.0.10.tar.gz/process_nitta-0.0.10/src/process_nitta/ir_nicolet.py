import pandas as pd

from .csv_config import CSVConfig
from .models import Base


class IRNICOLETSample(Base):
    def get_result_df(self) -> pd.DataFrame:
        df = pd.read_csv(
            self.file_path,
            **CSVConfig().IR_NICOLET().to_dict(),
        )
        return df
