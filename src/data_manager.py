import os
import pandas as pd

class DataManager:

    def __init__(self):
        self._transactions_df = None

    def load_csv(self, path) -> pd.DataFrame:
        df = pd.read_csv(path)
        return df

    def load_transaction(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported")
        
        df = pd.read_csv(file_path)

        self._validate_columns(df)
        self._transactions_df = df

        print('='*60,"\nDataset loaded successfully")

        return df

    def _validate_columns(self, df: pd.DataFrame):

        required_columns = {
            'step',
            'type',
            'amount',
            'nameOrig',
            'nameDest',
            'isFraud',
            'isFlaggedFraud'
        }

        missing_columns = required_columns - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Dataset is missing required column : {missing_columns}"
            )
        
    def get_transactoins(self) -> pd.DataFrame:

        if self.get_transactoins is None:
            raise RuntimeError("no dataset loaded yet.")
        
        return self._transactions_df.copy()
    
    def is_loaded(self) -> bool:
        return self._transactions_df is not None