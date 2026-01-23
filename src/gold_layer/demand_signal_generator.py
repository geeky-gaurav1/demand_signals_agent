import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib

# 🔹 AI Agent
from src.ai_agent.severity_refinement_agent import refine_severity

# -------------------------------
# High Risk Action Mapping
# -------------------------------
HIGH_RISK_ACTIONS = {
    "HIGH_SALES_VELOCITY_LOW_INVENTORY": "Trigger immediate replenishment",
    "LOW_INVENTORY_RISK": "Expedite stock transfer or reorder",
    "REVENUE_SPIKE_MARGIN_RISK": "Review pricing and supplier contracts",
    "CRITICAL_AI_RISK": "Escalate to demand planning team"
}


# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

IN_FILE = BASE_DIR / "data" / "clean" / "demand_signal_clean.csv"
OUT_DIR = BASE_DIR / "data" / "gold"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BATCH_TS = datetime.utcnow()

# -------------------------------
# Utilities
# -------------------------------
def generate_signal_id(row):
    """
    Deterministic business key for idempotency
    """
    raw = f"{row['sku_id']}_{row['store_id']}_{row['txn_date']}"
    return hashlib.md5(raw.encode()).hexdigest()

# -------------------------------
# Demand Signal Logic
# -------------------------------
def generate_demand_signal():

    print("🥇 Generating Gold layer demand signals")
    print("Running file:", __file__)

    df = pd.read_csv(IN_FILE)

    # -------------------------------
    # Derived metrics
    # -------------------------------
    df["sales_inventory_ratio"] = df["sales_qty"] / df["inventory_qty"]
    df["margin_pct"] = df["margin"] / df["revenue"]

    # Revenue percentiles (batch-level)
    rev_75 = df["revenue"].quantile(0.75)
    rev_90 = df["revenue"].quantile(0.90)

    # -------------------------------
    # Initialize outputs
    # -------------------------------
    df["signal_type"] = "NORMAL"
    df["severity"] = 1
    df["signal_reason"] = "Normal operating conditions"

    # =====================================================
    # Severity 3 (Highest Priority)
    # =====================================================
    cond_high_velocity_low_inv = (
        (df["sales_inventory_ratio"] >= 0.8) &
        (df["inventory_qty"] <= 5)
    )

    df.loc[cond_high_velocity_low_inv, ["signal_type", "severity", "signal_reason"]] = [
        "HIGH_SALES_VELOCITY_LOW_INVENTORY", 3,
        "Sales velocity very high with critically low inventory"
    ]

    cond_low_inventory = (
        (df["inventory_qty"] <= 5) & (~cond_high_velocity_low_inv)
    )

    df.loc[cond_low_inventory, ["signal_type", "severity", "signal_reason"]] = [
        "LOW_INVENTORY_RISK", 3,
        "Inventory critically low"
    ]

    cond_revenue_spike_margin_risk = (
        (df["revenue"] >= rev_90) &
        (df["margin_pct"] < 0.10)
    )

    df.loc[cond_revenue_spike_margin_risk, ["signal_type", "severity", "signal_reason"]] = [
        "REVENUE_SPIKE_MARGIN_RISK", 3,
        "High revenue observed with poor margin"
    ]

    # =====================================================
    # Severity 2
    # =====================================================
    cond_moderate_velocity = (
        (df["sales_inventory_ratio"] >= 0.5) &
        (df["sales_inventory_ratio"] < 0.8) &
        (df["severity"] == 1)
    )

    df.loc[cond_moderate_velocity, ["signal_type", "severity", "signal_reason"]] = [
        "MODERATE_SALES_VELOCITY", 2,
        "Sales velocity moderately high"
    ]

    cond_inventory_warning = (
        (df["inventory_qty"].between(6, 15)) &
        (df["severity"] == 1)
    )

    df.loc[cond_inventory_warning, ["signal_type", "severity", "signal_reason"]] = [
        "INVENTORY_WARNING", 2,
        "Inventory in warning range"
    ]

    cond_revenue_elevated = (
        (df["revenue"] >= rev_75) &
        (df["revenue"] < rev_90) &
        (df["severity"] == 1)
    )

    df.loc[cond_revenue_elevated, ["signal_type", "severity", "signal_reason"]] = [
        "REVENUE_ELEVATED", 2,
        "Revenue higher than normal"
    ]

    # =====================================================
    # 🤖 AI Severity Refinement (Foundry Hook) - apply only here
    # =====================================================
    df = refine_severity(df)


    # =====================================================
    # 🚨 Terminal High-Risk Action Notifications
    # =====================================================
    high_risk_df = df[df["severity"] >= 3]

    if not high_risk_df.empty:
        print("\n🚨 HIGH RISK DEMAND SIGNALS – ACTION REQUIRED 🚨")
        print("=" * 90)

        for _, row in high_risk_df.iterrows():
            action = HIGH_RISK_ACTIONS.get(
                row["signal_type"],
                "Immediate business review required"
            )

            print(
                f"SKU: {row['sku_id']} | "
                f"Store: {row['store_id']} | "
                f"Severity: {row['severity']} | "
                f"Signal: {row['signal_type']}\n"
                f"Reason: {row['signal_reason']}\n"
                f"Recommended Action: {action}"
            )
            print("-" * 90)
    else:
        print("\n✅ No high-risk demand signals detected in this batch")


    # =====================================================
    # 🔑 Signal Identity & Deduplication
    # =====================================================
    df["signal_id"] = df.apply(generate_signal_id, axis=1)
    df = df.drop_duplicates(subset=["signal_id"])

    # -------------------------------
    # Finalize Gold Dataset
    # -------------------------------
    df["gold_insert_ts"] = BATCH_TS

    out_file = OUT_DIR / "demand_signal_gold.csv"
    df.to_csv(out_file, index=False)

    print(f"✅ Gold layer file generated → {out_file}")
    print(f"📊 Total signals generated: {len(df)}")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    generate_demand_signal()
