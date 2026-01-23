import random
import pandas as pd
from faker import Faker
from datetime import date

fake = Faker()

def generate_finance_data(skus, n=300):
    data = []
    for i in range(n):
        revenue = round(random.uniform(100, 5000), 2)
        cost = round(revenue * random.uniform(0.6, 0.9), 2)
        data.append({
            "finance_id": i + 1,
            "sku_id": random.choice(skus),
            "posting_date": fake.date_between(
                start_date=date(2026, 1, 1), 
                end_date=date(2026, 12, 31)
            ),
            "revenue": revenue,
            "cost": cost,
            "margin": round(revenue - cost, 2),
            "source": "finance_system"
        })
    return pd.DataFrame(data)
