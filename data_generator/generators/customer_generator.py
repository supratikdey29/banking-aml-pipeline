import random
from datetime import datetime

def generate_customer(customer_id):

    first_names = ["John", "Mary", "Alex", "Priya", "James", "Robert", "Linda", "Michael", "Sara","Arjun","Sameer","Ajay","Rakesh","Paul","Albert","Chloe","Michelle","Missy","Cathy","Marina","Dhruv","Virat","Alex","Reese","Shiny"]
    last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Garcia","Roy","Nathan","David","Mission","Bell","Dey","Sen","Lazzo","Mochi","Minto","Lopez","Pablo","Escobar","Shaun","Ahuja"]
    CITIES = ["Dallas", "Plano", "Austin", "Irving","Frisco", "Houston", "San Antonio"]


    return {

        "customer_id": f"C{customer_id:04d}",

        "first_name": random.choice(first_names),

        "last_name": random.choice(last_names),

        "email": f"user{customer_id}@email.com",

        "phone": f"202-555-{random.randint(1000,9999)}",

        "city": random.choice(CITIES),

        "risk_score": round(random.uniform(0, 1), 2),

        "created_at": datetime.utcnow().isoformat()
    }