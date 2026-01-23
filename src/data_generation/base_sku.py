from faker import Faker

fake = Faker()

def generate_skus(n=50):
    return [f"SKU-{fake.unique.bothify(text='??###')}" for _ in range(n)]
