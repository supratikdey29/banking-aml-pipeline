import random
from datetime import datetime

def generate_merchant(merchant_id):

    merchants = [
        ("Walmart", "RETAIL"),
        ("Amazon", "E_COMMERCE"),
        ("Starbucks", "FOOD"),
        ("Shell Gas", "FUEL"),
        ("Apple Store", "TECH"),
        ("Target", "RETAIL"),
        ("Dollar Tree", "RETAIL"),
        ("Shipley", "FOOD"),
        ("Costco", "RETAIL"),
        ("Five Below", "RETAIL"),
        ("Home Depot", "RETAIL"),
        ("Lowes", "RETAIL"),
        ("Kirkland", "RETAIL"),
        ("RHCP", "FOOD"),
        ("Panera Bread", "FOOD"),
        ("AT&T", "TELECOM"),
        ("Verizon", "TELECOM"),
        ("Abids", "RETAIL"),
        ("7-11", "FUEL"),
        ("Love's", "FUEL"),
        ("ATMOS", "UTILITY"),
        ("Great Clips", "SERVICE"),
        ("Hideaway PIzza", "FOOD"),
        ("Mckinney City", "UTILITY"),
        ("CVS", "PHARMACY"),
        ("VAPE-SHAPE", "SERVICE"),
        ("NOORA's", "FOOD"),
        ("UPSIDE DOWN", "ENTERTAINMENT"),

    ]

    name, mtype = random.choice(merchants)

    return {

        "merchant_id": f"M{merchant_id:04d}",

        "merchant_name": name,

        "merchant_type": mtype,

        "country": "USA",

        "created_at": datetime.utcnow().isoformat()
    }