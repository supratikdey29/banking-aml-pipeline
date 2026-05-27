import random
from datetime import datetime

from data_generator.utils.id_generator import generate_account_id
from data_generator.generators.product_generator import generate_product_by_type


def generate_accounts(customer_id, account_start_id, num_accounts=2):

    accounts = []

    for i in range(num_accounts):

        account_type = random.choice(["CHECKING", "SAVINGS"])

        product = generate_product_by_type(account_type)

        account = {

            "account_id": generate_account_id(account_start_id + i),

            "customer_id": customer_id,

            "account_type": account_type,

            "product_code": product["product_code"],

            "product_name": product["product_name"],

            "risk_level": product["risk_level"],

            "balance": round(random.uniform(1000, 50000), 2),

            "status": "ACTIVE",

            "opened_date": datetime.utcnow().isoformat()
        }

        accounts.append(account)

    return accounts