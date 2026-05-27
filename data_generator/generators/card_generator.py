import random
from datetime import datetime

from data_generator.utils.id_generator import generate_card_id
from data_generator.generators.product_generator import generate_product_by_type


def generate_card(customer_id, account_id, card_number):

    product = generate_product_by_type("CREDIT_CARD")

    card_type = random.choice(["DEBIT", "CREDIT"])

    return {

        "card_id": generate_card_id(card_number),

        "customer_id": customer_id,

        "account_id": account_id,

        "product_code": product["product_code"],

        "product_name": product["product_name"],

        "card_type": card_type,

        "credit_limit": round(random.uniform(2000, 20000), 2),

        "status": "ACTIVE",

        "issued_date": datetime.utcnow().isoformat()
    }