import random
import pandas as pd
from faker import Faker

fake = Faker()

def generate_pos_data(skus, n=500):
    data = []
    for i in range(n):
        data.append({
            "pos_txn_id": i + 1,
            "sku_id": random.choice(skus + ["SKU-INVALID"]),
            "txn_date": fake.date_between(start_date="-30d", end_date="today"),
            "quantity_sold": random.randint(1, 15),
            "store_id": f"STORE-{random.randint(1, 50)}",
            "region": fake.state(),
            "source": "pos_system"
        })
    return pd.DataFrame(data)
