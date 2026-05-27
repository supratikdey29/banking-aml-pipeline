import random
from datetime import datetime

def generate_account_event(account_id, customer_id):

    event_types = [
        "LOGIN",
        "LOGOUT",
        "PASSWORD_CHANGE",
        "ADDRESS_UPDATE",
        "MOBILE_UPDATE",
        "FAILED_LOGIN"
    ]

    return {

        "event_id": f"EVT_{account_id}_{random.randint(1000,9999)}",

        "account_id": account_id,

        "customer_id": customer_id,

        "event_type": random.choice(event_types),

        "event_timestamp": datetime.utcnow().isoformat(),

        "source": random.choice(["MOBILE", "WEB", "ATM"])
    }