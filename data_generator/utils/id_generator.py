def generate_customer_id(number):
    return f"CUST{number:08d}"


def generate_account_id(number):
    return f"ACC{number:08d}"


def generate_transaction_id(number):
    return f"TXN{number:012d}"


def generate_card_id(number):
    return f"CARD{number:08d}"


def generate_loan_id(number):
    return f"LOAN{number:08d}"