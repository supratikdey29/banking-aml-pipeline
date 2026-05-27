from datetime import datetime
from data_generator.generators.transaction_generator import generate_transactions

account = {
    "account_id": "ACC00000001"
}

transactions = generate_transactions(
    account=account,
    customer_id="CUST00000001",
    txn_start_id=1,
    num_txns=10,
    base_date=datetime.utcnow()
)

for t in transactions:
    print(t)