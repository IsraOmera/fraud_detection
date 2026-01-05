import pandas as pd
from datetime import datetime
import os

class ReportGenerator:

    def export_csv(self, df:pd.DataFrame, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print('='*60 ,f'\nsaved csv to {filepath}')

    def generate_text_report(self, user_df:pd.DataFrame, filepath: str):

        now =datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total_users = len(user_df)
        # suspicious_users = user_df['user_is_suspicious'].sum()

        risk_distribution = (user_df['risk_band'].value_counts().to_dict() )

        top_risky_users = (user_df.sort_values('risk_score', ascending=False).head(10) )

        with open(filepath, "w") as f:
            f.write("Bank Transaction Risk & Anomaly Analyzer Report\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Generated at: {now}\n\n")

            f.write("Summary Statistics\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total users analyzed: {total_users}\n")
            # f.write(f"Suspicious users detected: {suspicious_users}\n\n")

            f.write("Risk Band Distribution\n")
            f.write("-" * 20 + "\n")
            for band, count in risk_distribution.items():
                f.write(f"{band}: {count}\n")
            f.write("\n")

            f.write("Top 10 High-Risk Users\n")
            f.write("-" * 20 + "\n")
            for _, row in top_risky_users.iterrows():
                f.write(
                    f"User: {row['nameOrig']} | "
                    f"Risk Band: {row['risk_band']} | "
                    f"Risk Score: {row['risk_score']:.3f} \n"
                )
                #  f"Suspicious Transactions: {row['suspicious_tx_count']}

            f.write("\nEnd of Report\n")
