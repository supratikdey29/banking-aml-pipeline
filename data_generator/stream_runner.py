from datetime import datetime
import random

from data_generator.generators.customer_generator import generate_customer
from data_generator.generators.account_generator import generate_accounts
from data_generator.generators.transaction_generator import generate_transactions
from data_generator.generators.card_generator import generate_card
from data_generator.generators.loan_generator import generate_loan
from data_generator.generators.account_event_generator import generate_account_event
from data_generator.generators.merchant_generator import generate_merchant

from data_generator.producers.kafka_producer import KafkaProducerClient
from data_generator.state_store import StateStore
from data_generator.utils.event_metadata import add_event_metadata


class BankingStreamRunner:

    def __init__(self):

        self.producer = KafkaProducerClient()
        self.state = StateStore()

    # =====================================================
    # RESET FOR FULL REPLAY (OPTIONAL)
    # =====================================================
    def reset_state_for_replay(self, reset_json=False):

        print("RESETTING STATE FOR REPLAY MODE")

        if reset_json:

            self.state.customers = {}
            self.state.accounts = {}
            self.state.cards = {}
            self.state.loans = {}
            self.state.merchants = {}

            self.state.counters = {
                "customer": 1,
                "account": 1,
                "card": 1,
                "loan": 1,
                "merchant": 1,
                "transaction": 1
            }

            self.state.save_state()

        print("STATE RESET COMPLETE")

    # =====================================================
    # INIT MERCHANTS (ONE TIME)
    # =====================================================
    def init_merchants(self):

        if len(self.state.merchants) > 0:
            return

        print("Initializing merchants...")

        for _ in range(10):

            merchant_id = self.state.next_id("merchant")

            merchant = generate_merchant(merchant_id)

            merchant["status"] = "ACTIVE"

            merchant = add_event_metadata(
                merchant,
                event_type="INSERT"
            )

            self.state.add_merchant(merchant)

            self.producer.send(
                topic="bank.merchants",
                key=merchant["merchant_id"],
                value=merchant
            )

    # =====================================================
    # CUSTOMER UPDATES (REAL CDC)
    # =====================================================
    def update_existing_customers(self, update_pct=0.1):

        customers = list(self.state.customers.values())

        if not customers:
            return

        num_updates = max(1, int(len(customers) * update_pct))

        selected = random.sample(customers, num_updates)

        for cust in selected:

            updated = cust.copy()

            field = random.choice([
                "email",
                "phone_number",
                "city",
                "risk_rating"
            ])

            if field == "email":
                updated[field] = f"upd_{random.randint(1000,9999)}@mail.com"

            elif field == "phone_number":
                updated[field] = f"+1-469-{random.randint(100,999)}-{random.randint(1000,9999)}"

            elif field == "city":
                updated[field] = random.choice([
                    "Dallas", "Plano", "Austin", "Irving", "Frisco"
                ])

            elif field == "risk_rating":
                updated[field] = random.choice([
                    "LOW", "MEDIUM", "HIGH"
                ])

            updated["updated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            updated = add_event_metadata(updated, event_type="UPDATE")

            self.state.upsert_customer(updated)

            self.producer.send(
                topic="bank.customers",
                key=updated["customer_id"],
                value=updated
            )

    # =====================================================
    # ACCOUNT CLOSURE (DELETE EVENT)
    # =====================================================
    def close_random_accounts(self, closure_pct=0.05):

        active_accounts = [
            a for a in self.state.accounts.values()
            if a.get("status") == "ACTIVE"
        ]

        if not active_accounts:
            return

        num_close = max(1, int(len(active_accounts) * closure_pct))

        selected = random.sample(active_accounts, num_close)

        for acc in selected:

            updated = acc.copy()

            updated["status"] = "CLOSED"
            updated["closed_date"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            updated = add_event_metadata(updated, event_type="DELETE")

            self.state.update_account(updated["account_id"], updated)

            self.producer.send(
                topic="bank.accounts",
                key=updated["account_id"],
                value=updated
            )

    # =====================================================
    # NEW CUSTOMERS + ENTITIES
    # =====================================================
    def create_new_customers(
        self,
        business_date,
        new_customers=5,
        accounts_per_customer=2
    ):

        for _ in range(new_customers):

            cid = self.state.next_id("customer")

            customer = generate_customer(cid)

            customer["business_date"] = business_date.strftime("%Y-%m-%d")
            customer["status"] = "ACTIVE"

            customer = add_event_metadata(customer, event_type="INSERT")

            customer = self.state.upsert_customer(customer)

            self.producer.send(
                topic="bank.customers",
                key=customer["customer_id"],
                value=customer
            )

            # -----------------------------
            # LOANS
            # -----------------------------
            lid = self.state.next_id("loan")

            loan = generate_loan(customer["customer_id"], lid)

            loan["business_date"] = business_date.strftime("%Y-%m-%d")
            loan["status"] = "ACTIVE"

            loan = add_event_metadata(loan, event_type="INSERT")

            self.state.add_loan(loan)

            self.producer.send(
                topic="bank.loans",
                key=loan["loan_id"],
                value=loan
            )

            # -----------------------------
            # ACCOUNTS
            # -----------------------------
            accounts = generate_accounts(
                customer["customer_id"],
                self.state.next_id("account"),
                accounts_per_customer
            )

            for acc in accounts:

                acc["business_date"] = business_date.strftime("%Y-%m-%d")
                acc["status"] = "ACTIVE"

                acc = add_event_metadata(acc, event_type="INSERT")

                self.state.add_account(acc)

                self.producer.send(
                    topic="bank.accounts",
                    key=acc["account_id"],
                    value=acc
                )

                # -----------------------------
                # CARDS
                # -----------------------------
                card_id = self.state.next_id("card")

                card = generate_card(
                    customer["customer_id"],
                    acc["account_id"],
                    card_id
                )

                card["business_date"] = business_date.strftime("%Y-%m-%d")
                card["status"] = "ACTIVE"

                card = add_event_metadata(card, event_type="INSERT")

                self.state.add_card(card)

                self.producer.send(
                    topic="bank.cards",
                    key=card["card_id"],
                    value=card
                )

                # -----------------------------
                # ACCOUNT EVENTS
                # -----------------------------
                event = generate_account_event(
                    acc["account_id"],
                    customer["customer_id"]
                )

                event["business_date"] = business_date.strftime("%Y-%m-%d")

                event = add_event_metadata(event, event_type="INSERT")

                self.producer.send(
                    topic="bank.account_events",
                    key=event["event_id"],
                    value=event
                )

    # =====================================================
    # TRANSACTIONS (DAILY + FRAUD)
    # =====================================================
    def generate_daily_transactions(
        self,
        business_date,
        txns_per_account=10,
        fraud_ratio=0.05
    ):

        active_accounts = [
            a for a in self.state.accounts.values()
            if a.get("status") == "ACTIVE"
        ]

        for acc in active_accounts:

            start_id = self.state.next_id("transaction")

            txns = generate_transactions(
                account=acc,
                customer_id=acc["customer_id"],
                txn_start_id=start_id,
                num_txns=txns_per_account,
                base_date=business_date
            )

            for txn in txns:

                txn["business_date"] = business_date.strftime("%Y-%m-%d")
                txn["status"] = "ACTIVE"

                if random.random() < fraud_ratio:

                    txn["amount"] = round(random.uniform(10000, 50000), 2)
                    txn["merchant"] = "CRYPTO_EXCHANGE"
                    txn["transaction_type"] = "WIRE_TRANSFER"
                    txn["location"] = random.choice(["PANAMA", "CAYMAN", "DUBAI"])
                    txn["aml_flag"] = "SUSPICIOUS"
                else:
                    txn["aml_flag"] = "NORMAL"

                txn = add_event_metadata(txn, event_type="INSERT")

                self.producer.send(
                    topic="bank.transactions",
                    key=txn["transaction_id"],
                    value=txn
                )

    # =====================================================
    # MAIN ORCHESTRATION
    # =====================================================
    def run_batch(
        self,
        business_date,
        new_customers=5,
        accounts_per_customer=2,
        txns_per_account=10,
        fraud_ratio=0.05,
        customer_update_pct=0.1,
        account_closure_pct=0.05
    ):

        print("\n====================================")
        print(f"BATCH FOR {business_date}")
        print("====================================\n")

        self.init_merchants()

        self.create_new_customers(
            business_date,
            new_customers,
            accounts_per_customer
        )

        self.update_existing_customers(customer_update_pct)

        self.close_random_accounts(account_closure_pct)

        self.generate_daily_transactions(
            business_date,
            txns_per_account,
            fraud_ratio
        )

        self.producer.flush()

        print("\nBATCH COMPLETE\n")