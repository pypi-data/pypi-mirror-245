import pandas as pd

from .csv_config import CSVConfig
from .models import Base


class RamanSample(Base):
    def get_result_df(self):
        return pd.read_csv(self.file_path, **CSVConfig().Raman().to_dict())
