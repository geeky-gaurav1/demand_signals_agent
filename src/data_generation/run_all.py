from pathlib import Path

from base_sku import generate_skus
from pos_generator import generate_pos_data
from inventory_generator import generate_inventory_data
from finance_generator import generate_finance_data

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Raw data path
RAW_DATA_PATH = BASE_DIR / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

# Generate SKUs
skus = generate_skus()

# Generate datasets
pos_df = generate_pos_data(skus)
inventory_df = generate_inventory_data(skus)
finance_df = generate_finance_data(skus)

# Save CSVs
pos_df.to_csv(RAW_DATA_PATH / "pos_data.csv", index=False)
inventory_df.to_csv(RAW_DATA_PATH / "inventory_data.csv", index=False)
finance_df.to_csv(RAW_DATA_PATH / "finance_data.csv", index=False)

print("✅ POS, Inventory, Finance datasets generated successfully.")
