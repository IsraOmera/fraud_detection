import numpy as np
import pandas as pd
from scipy.stats import zscore

class RiskScorer:

    risk_features = [
        'tsc_count',
        'total_amount', 
        'avg_amount',
        'max_amount',
        'std_amount',
        'tsc_per_day',
        'rolling_mean_24h',
        'rolling_std_24h',
        'suspicious_tsc_count',
        'suspicious_tx_ratio'
    ]

    def __init__(self, 
                 max_risk_threshold = 0.9, 
                 suspicious_ratio_threshold = 0.3,
                 min_suspiscious_tx = 3) -> None:
        
        self.max_risk_threshold = max_risk_threshold
        self.suspicious_ratio_threshold = suspicious_ratio_threshold
        self.min_suspiscious_tx = min_suspiscious_tx

    def score(self, features_df: pd.DataFrame) -> pd.DataFrame:
        df = features_df.copy()

        df = self._check_features(df)
        df = self._compute_z_scores(df)
        df = self._compute_risk_score(df)
        df = self._flag_user(df)
        df = self._assign_risk_band(df)

        print("Risk scoring completed")
        return df

    def _check_features(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = set(self.risk_features) - set(df.columns)

        if missing:
            raise ValueError(f"Misssing risk features: {missing}")
        
        df[self.risk_features] = df[self.risk_features].fillna(0)

        return df
    
    def _compute_z_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        z_values = zscore(df[self.risk_features], nan_policy = 'omit')

        z_df = pd.DataFrame(
            np.abs(z_values),
            columns = [f'z_{c}' for c in self.risk_features],
            index = df.index
        )

        return pd.concat([df, z_df], axis=1)
    
    def _compute_risk_score(self, df: pd.DataFrame) -> pd.DataFrame:
        z_cols = [c for c in df.columns if c.startswith('z_')]
        df['risk_score'] = df[z_cols].mean(axis = 1)

        return df
    
    def _flag_user(self, df : pd.DataFrame) -> pd.DataFrame:
       
        df['user_is_suspicious'] = (
            (df['risk_score'] >= self.max_risk_threshold)&
            (df['suspicious_tsc_count'] >= self.min_suspiscious_tx)&
            (df['suspicious_tx_ratio'] >= self.suspicious_ratio_threshold)
            ).astype(int)
        
        return df

    
    def _assign_risk_band(self, df: pd.DataFrame) -> pd.DataFrame:

        conditions = [
            df['risk_score'] < 1,
            df['risk_score'].between(1,2, inclusive= 'left'),
            df['risk_score'].between(2,3, inclusive='left'),
            df['risk_score'] >= 3
        ]

        bands = ['Low', 'Medium', 'High', 'Critical']

        df['risk_band'] = np.select(conditions, bands, default='Unknown')

        return df


















