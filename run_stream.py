from datetime import datetime, timedelta
from data_generator.stream_runner import BankingStreamRunner


# =====================================================
# UTIL: DATE RANGE
# =====================================================
def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d")


def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":

    print("\n===================================")
    print("BANKING AML STREAM SIMULATOR (SAFE MODE)")
    print("===================================\n")

    runner = BankingStreamRunner()

    # =========================
    # RESET CONTROL (SAFE)
    # =========================
    reset_choice = input("Do you want FULL RESET before running? (y/n): ")

    if reset_choice.lower() == "y":

        reset_json = input("Also reset JSON state store? (y/n): ")

        runner.reset_state_for_replay(
            reset_json=True if reset_json.lower() == "y" else False
        )

    # =========================
    # MODE SELECTION
    # =========================
    mode = input("\nRun mode (1=single day, 2=date range): ")

    # =================================================
    # SINGLE DAY MODE
    # =================================================
    if mode == "1":

        business_date = parse_date(
            input("Enter business date (YYYY-MM-DD): ")
        )

        runner.run_batch(
            business_date=business_date,
            new_customers=int(input("New customers: ")),
            accounts_per_customer=int(input("Accounts per customer: ")),
            txns_per_account=int(input("Transactions per account: ")),
            fraud_ratio=float(input("Fraud ratio: ")),
            customer_update_pct=float(input("Customer update pct: ")),
            account_closure_pct=float(input("Account closure pct: "))
        )

    # =================================================
    # DATE RANGE MODE (REPLAY / BACKFILL)
    # =================================================
    elif mode == "2":

        start_date = parse_date(
            input("Start date (YYYY-MM-DD): ")
        )

        end_date = parse_date(
            input("End date (YYYY-MM-DD): ")
        )

        new_customers_per_day = int(input("New customers per day: "))
        accounts_per_customer = int(input("Accounts per customer: "))
        txns_per_account = int(input("Transactions per account: "))
        fraud_ratio = float(input("Fraud ratio: "))
        customer_update_pct = float(input("Customer update pct: "))
        account_closure_pct = float(input("Account closure pct: "))

        print("\nStarting historical replay...\n")

        for d in date_range(start_date, end_date):

            print("\n===================================")
            print(f"DATE: {d.date()}")
            print("===================================\n")

            runner.run_batch(
                business_date=d,
                new_customers=new_customers_per_day,
                accounts_per_customer=accounts_per_customer,
                txns_per_account=txns_per_account,
                fraud_ratio=fraud_ratio,
                customer_update_pct=customer_update_pct,
                account_closure_pct=account_closure_pct
            )

    else:
        print("Invalid mode selected")