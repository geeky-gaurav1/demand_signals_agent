import pandas as pd

def refine_severity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulated Foundry AI Agent:
    - Can downgrade severity
    - Cannot upgrade above 3
    - Adds AI explanation
    """

    df = df.copy()

    df["ai_adjusted_severity"] = df["severity"]
    df["ai_explanation"] = "Rule-based severity applied"

    # Example AI logic (controlled & explainable)
    downgrade_condition = (
        (df["severity"] == 3) &
        (df["inventory_qty"] > 20) &
        (df["margin_pct"] > 0.25)
    )

    df.loc[downgrade_condition, "ai_adjusted_severity"] = 2
    df.loc[downgrade_condition, "ai_explanation"] = (
        "Historically sufficient inventory and healthy margin detected; urgency reduced"
    )

    return df
