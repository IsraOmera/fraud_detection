# Fraud Detection Pipeline (Python)

This project implements an end-to-end **fraud detection feature engineering and analysis pipeline** using Python and pandas.  
It is designed to process transaction data, engineer customer-level risk features, flag suspicious activity, and export clean datasets for modeling or reporting.

---

## 📁 Project Structure

fraud_detection/
│
├── data/
│ ├── raw/ # Original datasets
│ ├── processed/ # Cleaned & feature-engineered data
│
├── reports/ # Generated CSV reports
│
├── src/
│ ├── cleaner.py # Data cleaning logic
│ ├── feature_builder.py # Feature engineering (velocity, rolling, risk)
│ ├── report_generator.py# CSV export utilities
│ ├── console_app.py # CLI orchestration
│
├── main.py # Application entry point
├── requirements.txt
├── README.md


---

## 🚀 Features Implemented

### ✅ Transaction-Level
- Fraud & flagged-fraud detection
- Suspicious transaction labeling
- Rolling transaction statistics (24h window)

### ✅ Customer-Level
- Transaction count
- Total, average, max, std transaction amount
- Velocity features (transactions per active day)
- Suspicious transaction ratio
- Rolling behavioral statistics

---

## 🧠 Feature Engineering Overview

| Feature | Description |
|------|------------|
| `tsc_count` | Total transactions per user |
| `total_amount` | Total transaction value |
| `avg_amount` | Mean transaction amount |
| `tsc_per_day` | Transaction velocity |
| `rolling_mean_24h` | Rolling mean over last 24 hours |
| `suspicious_tx_ratio` | Ratio of suspicious transactions |

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt

Run the application

python main.py


Processed datasets are saved to:
data/processed/

reports datasets and texts are saved to:
reports/

Technologies Used

Python 3.9+

pandas

numpy

pathlib