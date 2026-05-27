import random
from datetime import datetime, timedelta

def generate_transactions(account, customer_id, txn_start_id, num_txns, base_date):

    txns = []

    categories = [
        "ATM_WITHDRAWAL",
        "DEPOSIT",
        "ONLINE_PURCHASE",
        "POS_PURCHASE",
        "ACH_TRANSFER",
        "WIRE_TRANSFER"
    ]

    for i in range(num_txns):

        txn_time = base_date - timedelta(minutes=random.randint(0, 1440))

        txns.append({

            "transaction_id": f"T{txn_start_id + i:06d}",

            "account_id": account["account_id"],

            "customer_id": customer_id,

            "amount": round(random.uniform(10, 2000), 2),

            "currency": "USD",

            "transaction_type": random.choice(categories),

            "merchant": random.choice([
                "Walmart", "Amazon", "Starbucks", "Shell Gas", "Apple Store"
            ]),

            "transaction_timestamp": txn_time.isoformat(),

            "location": random.choice(["TX", "NY", "CA", "FL"]),

            "status": "SUCCESS",

            "flag": "NORMAL"
        })

    return txns