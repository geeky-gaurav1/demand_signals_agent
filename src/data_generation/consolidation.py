import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "data" / "consolidated"

def consolidate():

    pos = pd.read_csv(RAW_DIR / "pos_data.csv")
    inventory = pd.read_csv(RAW_DIR / "inventory_data.csv")
    finance = pd.read_csv(RAW_DIR / "finance_data.csv")

    # Normalize column names
    for df in (pos, inventory, finance):
        df.columns = df.columns.str.strip().str.lower()

    # Rename business columns to common names
    pos.rename(columns={"quantity_sold": "sales_qty"}, inplace=True)
    inventory.rename(columns={"stock_on_hand": "inventory_qty"}, inplace=True)

    # Safety check
    for name, df in [("pos", pos), ("inventory", inventory), ("finance", finance)]:
        if "sku_id" not in df.columns:
            raise ValueError(f"'sku' column missing in {name}")

    # consolidated = (
    #     pos.merge(inventory, on="sku", how="left", suffixes=("_pos", "_inv"))
    #        .merge(finance, on="sku", how="left", suffixes=("", "_fin"))
    # )
    consolidated = pos.merge(inventory, on="sku_id", how="left").merge(finance, on="sku_id", how="right")

    OUT_DIR.mkdir(exist_ok=True)
    consolidated.to_csv(OUT_DIR / "demand_signal_data.csv", index=False)

    print("✅ Consolidation completed successfully")

if __name__ == "__main__":
    consolidate()
