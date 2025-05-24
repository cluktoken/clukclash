import random

def get_price(token):
    random.seed(token)
    base = 10 if token == "BITS" else 5
    return base + random.random() * 5