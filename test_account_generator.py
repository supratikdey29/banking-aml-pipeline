from data_generator.generators.account_generator import generate_accounts

accounts = generate_accounts("CUST00000001", 1, 3)

for a in accounts:
    print(a)