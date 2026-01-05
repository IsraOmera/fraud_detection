from src.data_manager import DataManager
from src.transaction_cleaner import TransactionCleaner
from src.feature_builder import FeatureBuilder
from src.risk_scorer import RiskScorer
from src.report_generator import ReportGenerator

class ConsoleApp:
    def __init__(self) -> None:
        self.data_manager  = DataManager()
        self.cleaner = TransactionCleaner()
        self.feature_builder = FeatureBuilder()
        self.risk_scorer = RiskScorer()
        self.report_generator = ReportGenerator()

        self.raw_df = None
        self.cleaned_df = None
        self.customer_features = None
        self.scored_users = None
        self.flagged_transactions = None
        self.user_summary = None

    def display_menu(self):
        print("\n Bank Transaction Risk Analyzer ")
        print("1. Load dataset")
        print("2. Clean and validate data")
        print("3. Build features")
        print("4. Score transactions")
        print("5. Score stored features")
        print("6. Export reports")
        print("7. Display summary")
        print("0. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Select an option: ")

            if choice == "1":
                self.load_data()
            elif choice == "2":
                self.clean_data()
            elif choice == "3":
                self.build_features()
            elif choice == "4":
                self.score_customers()
            elif choice == "5":
                self.score_stored_features()
            elif choice == "6":
                self.export_reports()
            elif choice == "7":
                self.display_summary()
            elif choice == "0":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Try again.")

    def load_data(self):
        # path = input("Enter path to CSV file: ")
        path = r"../data/raw/reduced_paysim.csv"
        
        try:
            self.raw_df = self.data_manager.load_transaction(path)
            print('='*60,f"\nShape: {self.raw_df.shape}\n",'='*60)        
        except FileNotFoundError as e: print(f"ERROR: {e}")

        except ValueError as e: print(f"ERROR: {e}")

        except Exception as e:
            print('='*60,f"\nUnexpected error while loading data.")
            print(e)

    def clean_data(self):
            if self.raw_df is None:
                print('='*60,f"\nLoad data first.")
                return
            
            self.cleaned_df = self.cleaner.clean(self.raw_df)
            print('='*60,f"\nData cleaned: {self.cleaned_df.shape}")
            self.report_generator.export_csv(self.cleaned_df,r"G:\iti\Python\fraud_detection\git\data\processed\clean.csv")

    def build_features(self):
        if self.cleaned_df is None:
            print('='*60,f"\nClean data first.")
            return
        
        self.customer_features = self.feature_builder.build_customer_feature(self.cleaned_df)
        self.report_generator.export_csv(self.customer_features,r"G:\iti\Python\fraud_detection\git\data\processed\customer_features2.csv")

        print('='*60,f"\nTransaction features built.")

    def score_customers(self):
        if self.customer_features is None:
            print('='*60,f"\nBuild features first.")
            return
        
        try:
            self.scored_users = self.risk_scorer.score(self.customer_features)
            self.report_generator.export_csv(self.scored_users,filename="customer_risk_summary1.csv")
            print('='*60,f"\nTransactions scored.")

        except ValueError as e: print(f"ERROR: {e}")

        except Exception as e:
            print('='*60,f"\nUnexpected error while loading data.")
            print(e)
    
    def score_stored_features(self):
        
        features_path = r"G:\iti\Python\fraud_detection\git\data\processed\customer_features2.csv"
        ready_customer_features = self.data_manager.load_csv(features_path)

        try:
            self.scored_users = self.risk_scorer.score(ready_customer_features)
            # self.report_generator.export_csv(self.scored_users,filename="customer_risk_summary1.csv")
            print('='*60,f"\nTransactions scored.")

        except ValueError as e: print(f"ERROR: {e}")

        except Exception as e:
            print('='*60,f"\nUnexpected error while loading data.")
            print(e)
        

    def export_reports(self):
        if self.scored_users is None:
            print('='*60,f"\nFlag users first.")
            return
        
        self.report_generator.export_csv(self.scored_users,filepath=r"G:\iti\Python\fraud_detection\git\reports\customer_risk_summary.csv")
        self.report_generator.generate_text_report(self.scored_users,filepath=r"G:\iti\Python\fraud_detection\git\reports\risk_report.txt")

        print('='*60,f"\nReports exported successfully.")

    def display_summary(self):
        if self.scored_users is None:
            print('='*60,f"\nNo summary available.")
            return
        
        print('='*60,f"\nTop Risky Users")
        print(self.scored_users.sort_values("risk_score", ascending=False).head(10)
              [['nameOrig', 'risk_band', 'risk_score']])
