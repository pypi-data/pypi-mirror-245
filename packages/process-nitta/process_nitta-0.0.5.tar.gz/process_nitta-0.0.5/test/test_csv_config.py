import pandas as pd
import pytest
from process_nitta.csv_config import CSVConfig


class TestInstronCSVConfig:
    def test_csv_config_instron_正常系(self):
        csv_config = CSVConfig().Instron().to_dict()
        pd.read_csv("./process-nitta/test/csv/instron.csv", **csv_config)

    def test_csv_config_instron_異常系_ファイルパスが存在しない(self):
        csv_config = CSVConfig().Instron().to_dict()

        with pytest.raises(FileNotFoundError):
            pd.read_csv("invalid_path", **csv_config)


class TestAgisCSVConfig:
    def test_csv_config_agis_正常系(self):
        csv_config = CSVConfig().AGIS().to_dict()
        pd.read_csv("./process-nitta/test/csv/agis.csv", **csv_config)

    def test_csv_config_agis_異常系_ファイルパスが存在しない(self):
        csv_config = CSVConfig().AGIS().to_dict()

        with pytest.raises(FileNotFoundError):
            pd.read_csv("invalid_path", **csv_config)


class TestDmaCSVConfig:
    def test_csv_config_dma_正常系(self):
        csv_config = CSVConfig().DMA().to_dict()
        pd.read_csv("./process-nitta/test/csv/dma.csv", **csv_config)

    def test_csv_config_dma_異常系_ファイルパスが存在しない(self):
        csv_config = CSVConfig().DMA().to_dict()

        with pytest.raises(FileNotFoundError):
            pd.read_csv("invalid_path", **csv_config)


class TestIrCSVConfig:
    def test_csv_config_ir_正常系(self):
        csv_config = CSVConfig().IR().to_dict()
        pd.read_csv("./process-nitta/test/csv/ir.csv", **csv_config)

    def test_csv_config_ir_異常系_ファイルパスが存在しない(self):
        csv_config = CSVConfig().IR().to_dict()

        with pytest.raises(FileNotFoundError):
            pd.read_csv("invalid_path", **csv_config)
