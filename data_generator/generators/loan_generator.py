import random
from datetime import datetime

from data_generator.utils.id_generator import generate_loan_id
from data_generator.generators.product_generator import generate_product_by_type


def generate_loan(customer_id, loan_number):

    product = generate_product_by_type("LOAN")

    principal = round(random.uniform(5000, 200000), 2)

    return {

        "loan_id": generate_loan_id(loan_number),

        "customer_id": customer_id,

        "product_code": product["product_code"],

        "product_name": product["product_name"],

        "principal_amount": principal,

        "outstanding_balance": principal,

        "interest_rate": round(random.uniform(3, 12), 2),

        "tenure_months": random.choice([36, 60, 120]),

        "status": "ACTIVE",

        "created_at": datetime.utcnow().isoformat()
    }