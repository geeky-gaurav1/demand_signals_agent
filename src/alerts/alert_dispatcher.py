import pandas as pd
from pathlib import Path
from datetime import datetime

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
GOLD_FILE = BASE_DIR / "data" / "gold" / "demand_signal_gold.csv"

# -------------------------------
# Alert Dispatcher
# -------------------------------
def dispatch_alerts():

    print("🚨 Alert Dispatcher Started")
    print("Running file:", __file__)

    df = pd.read_csv(GOLD_FILE)

    # ⚠️ DO NOT re-apply refine_severity here
    # Trigger alerts ONLY for final severity 3
    alerts = df[df["ai_adjusted_severity"] == 3]

    if alerts.empty:
        print("✅ No critical alerts generated")
        return

    print(f"🔥 {len(alerts)} CRITICAL ALERT(S) DETECTED\n")

    for _, row in alerts.iterrows():
        print("=" * 70)
        print(f"ALERT TIME   : {datetime.now()}")
        print(f"SKU          : {row['sku']}")
        print(f"STORE / REG  : {row.get('store_id', 'NA')} / {row.get('region', 'NA')}")
        print(f"SIGNAL TYPE  : {row['signal_type']}")
        print(f"SEVERITY     : {row['ai_adjusted_severity']}")
        print(f"REASON       : {row['signal_reason']}")
        print(f"AI CONTEXT   : {row['ai_explanation']}")
        print("=" * 70)
        print()

    print("🚨 Alert dispatching completed")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    dispatch_alerts()
