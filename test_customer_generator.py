import json
from data_generator.generators.customer_generator import generate_customer

customers = []

for i in range(1, 6):
    customers.append(generate_customer(i))

print(json.dumps(customers, indent=2))