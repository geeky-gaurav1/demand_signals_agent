import pandas as pd
from pathlib import Path
from datetime import datetime

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

IN_FILE = BASE_DIR / "data" / "consolidated" / "demand_signal_data.csv"
CLEAN_DIR = BASE_DIR / "data" / "clean"
REJECT_DIR = BASE_DIR / "data" / "rejected"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REJECT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Batch Metadata
# -------------------------------
BATCH_TS = datetime.now()

# -------------------------------
# Helper Functions
# -------------------------------
def get_null_columns(row):
    return ",".join(row.index[row.isna()].tolist())


# -------------------------------
# Main Cleaning Logic
# -------------------------------
def clean_demand_signal_data():

    print("🚀 Running NEW data cleaning engine with rule priority")
    print("Running file:", __file__)

    df = pd.read_csv(IN_FILE)

    rejected_records = []

    # =====================================================
    # 1️⃣ NULL CHECK (Highest Priority)
    # =====================================================
    null_rows = df[df.isna().any(axis=1)].copy()

    if not null_rows.empty:
        null_rows["rejection_reason"] = null_rows.apply(
            lambda r: f"NULL_COLUMNS: {get_null_columns(r)}",
            axis=1
        )
        null_rows["record_insert_ts"] = BATCH_TS
        rejected_records.append(null_rows)

    df = df.dropna()

    # =====================================================
    # 2️⃣ DUPLICATE CHECK
    # =====================================================
    duplicate_rows = df[df.duplicated()].copy()

    if not duplicate_rows.empty:
        duplicate_rows["rejection_reason"] = "DUPLICATE_RECORD"
        duplicate_rows["record_insert_ts"] = BATCH_TS
        rejected_records.append(duplicate_rows)

    df = df.drop_duplicates()

    # =====================================================
    # 3️⃣ BUSINESS RULE CHECKS
    # =====================================================

    business_rejects = []

    # 3.1 Negative Value Checks
    negative_condition = (
        (df["sales_qty"] < 0) |
        (df["revenue"] < 0)
    )

    neg_rows = df[negative_condition].copy()

    if not neg_rows.empty:
        neg_rows["rejection_reason"] = "NEGATIVE_VALUE_DETECTED"
        neg_rows["record_insert_ts"] = BATCH_TS
        business_rejects.append(neg_rows)

    df = df[~negative_condition]

    # 3.2 Inventory < Sales Rule
    inventory_violation = df["inventory_qty"] < df["sales_qty"]

    inv_rows = df[inventory_violation].copy()

    if not inv_rows.empty:
        inv_rows["rejection_reason"] = "INVENTORY_LESS_THAN_SALES"
        inv_rows["record_insert_ts"] = BATCH_TS
        business_rejects.append(inv_rows)

    df = df[~inventory_violation]

    if business_rejects:
        rejected_records.append(pd.concat(business_rejects, ignore_index=True))

    # =====================================================
    # 4️⃣ Write Clean Data
    # =====================================================
    df["record_insert_ts"] = BATCH_TS

    clean_file = CLEAN_DIR / "demand_signal_clean.csv"
    df.to_csv(clean_file, index=False)

    print(f"✅ Clean data written → {clean_file}")

    # =====================================================
    # 5️⃣ Write Rejected Data
    # =====================================================
    if rejected_records:
        rejected_df = pd.concat(rejected_records, ignore_index=True)
        reject_file = REJECT_DIR / "demand_signal_rejected.csv"
        rejected_df.to_csv(reject_file, index=False)

        print(f"🚨 Rejected data written → {reject_file}")
    else:
        print("🎉 No rejected records found")

    print("✅ Data cleaning completed successfully")


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    clean_demand_signal_data()
