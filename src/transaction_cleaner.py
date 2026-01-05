import pandas as pd

class TransactionCleaner:

    valid_transaction_types = {
        'CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER'
    }

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
       
        df = self._remove_duplicates(df)
        df = self._handle_missing_values(df)
        df = self._validate_amount(df)
        df = self._validate_step(df)
        df = self._validate_transaction_type(df)
        df = self._cast_types(df)
        df = self._add_time_feature(df)

        return df
    
    def _remove_duplicates(self, df:pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)

        if before != after:
            print('='*60,f"\nRemoved {before - after} duplicate rows")
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:

        critical_columns = ['step', 'type', 'amount', 'nameOrig']
        df = df.dropna(subset=critical_columns)

        df['nameDest'] = df['nameDest'].fillna('UNKNOWN')

        return df
    
    def _validate_amount(self, df:pd.DataFrame) -> pd.DataFrame:
        df = df[df['amount'] > 0]

        return df
    
    def _validate_step(step, df:pd.DataFrame) -> pd.DataFrame:
        df = df[(df['step'] >=1) & (df['step'] <= 744)]

        return df
    
    def _validate_transaction_type(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df['type'].isin(self.valid_transaction_types)]

        return df
    
    def  _cast_types(self, df:pd.DataFrame) -> pd.DataFrame:
        df['step'] = df['step'].astype(int)
        df['amount'] = df['amount'].astype(float)
        df['type'] = df['type'].astype('category')

        return df
    
    def _add_time_feature(self, df: pd.DataFrame) -> pd.DataFrame:

        df['day'] = (df['step'] - 1) // 24 + 1
        df['hour'] = (df['step'] -1) % 24

        return df
    