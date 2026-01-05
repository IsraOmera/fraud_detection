import pandas as pd

class FeatureBuilder:

    def build_customer_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        print("1.0")
        df = self._flag_transactions(df)
        print('1.1')
        
        customer_stats = self._basic_aggregations(df)
        print('1.2')
        velocity_stats = self._velocity_feature(df)
        print('1.3')
        rolling_stats = self._rolling_features(df)
        print('1.4')
        flag_stats = self._flag_users(df)
        print('1.5')
        features = ( customer_stats.merge(velocity_stats, on = 'nameOrig', how = 'left')
                    .merge(rolling_stats, on = 'nameOrig', how = 'left')
                    .merge(flag_stats, on = 'nameOrig', how = 'left'))

        return features    

    def _flag_transactions(self, df : pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        print('2.0')

        fraudulent = (df['isFraud'] == 1) | (df['isFlaggedFraud'] == 1)
        print('2.1')
        df['is_suspicious'] = fraudulent.astype(int)
        print('2.2')

        return df
    
    def _basic_aggregations(self, df: pd.DataFrame) -> pd.DataFrame:
        print('3.0')
        agg_df = (
            df.groupby('nameOrig')['amount'].agg(
                tsc_count = 'count',
                total_amount = 'sum',
                avg_amount = 'mean',
                max_amount = 'max',
                std_amount = 'std'
            ).reset_index()
        )
        print('3.1')

        return agg_df
    
    def _velocity_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        
        print('4.0')
        active_days = (
            df.groupby('nameOrig')['day'].nunique().reset_index(name = 'active_days')
        )
        print('4.1')
        tsc_count = (
            df.groupby('nameOrig').size().reset_index(name = 'tsc_count')
        )
        print('4.2')
        velocity = active_days.merge(tsc_count, on= 'nameOrig')
        print('4.3')
        velocity['tsc_per_day'] = ( velocity['tsc_count'] / velocity['active_days'])
        print('4.4')
        return velocity[['nameOrig', 'active_days', 'tsc_per_day']]
    
    def _rolling_features(self, df: pd.DataFrame) -> pd.DataFrame:
        print('5.0')
        df = df.sort_values(['nameOrig', 'step'])
        print('5.1')
        rolling = (
            df.groupby('nameOrig')['amount'].rolling(window = 24, min_periods = 1 )
            .agg(['mean', 'std']).reset_index()
        )
        print('5.2')
        rolling =rolling.rename(columns={'mean':'rolling_mean_24h','std':'rolling_std_24h'})
        print('5.3')

        latest_rolling = (rolling.groupby('nameOrig').tail(1).reset_index(drop = True))
        print('5.4')
        return latest_rolling[['nameOrig', 'rolling_mean_24h', 'rolling_std_24h']]
    
    
    def _flag_users(self, df:pd.DataFrame)-> pd.DataFrame:
        print('6.0')
        user_flags = (df.groupby('nameOrig').agg(
            suspicious_tsc_count = ('is_suspicious', 'sum')) )
        print('6.1')
        tsc_count = (
            df.groupby('nameOrig').size().reset_index(name = 'tsc_count')
        )
        print('6.2')
        user_flags = user_flags.merge(tsc_count, on='nameOrig')
        print('6.3')
        user_flags['suspicious_tx_ratio'] = (
            user_flags['suspicious_tsc_count'] /  user_flags['tsc_count'].replace(0, pd.NA)
        )
        print('6.4')
        return user_flags[['nameOrig', 'suspicious_tsc_count', 'suspicious_tx_ratio']]

    