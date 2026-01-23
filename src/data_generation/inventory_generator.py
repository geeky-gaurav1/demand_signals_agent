import random
import pandas as pd
from faker import Faker

fake = Faker()

def generate_inventory_data(skus, n=200):
    data = []
    for i in range(n):
        data.append({
            "inventory_id": i + 1,
            "sku_id": random.choice(skus),
            "stock_on_hand": random.randint(0, 500),
            "warehouse": fake.city(),
            "last_updated": fake.date_between(start_date="-7d", end_date="today"),
            "source": "inventory_system"
        })
    return pd.DataFrame(data)
