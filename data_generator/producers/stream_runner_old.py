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


class BankingStreamRunner:

    def __init__(self):

        self.producer = KafkaProducerClient()
        self.state = StateStore()

        self.customer_counter = 1
        self.account_counter = 1
        self.transaction_counter = 1
        self.card_counter = 1
        self.loan_counter = 1
        self.merchant_counter = 1

    # -----------------------------
    # MERCHANTS (STATIC ONCE)
    # -----------------------------
    def init_merchants(self):

        if len(self.state.merchants) > 0:
            return

        for _ in range(10):

            merchant = generate_merchant(self.merchant_counter)

            self.state.add_merchant(merchant)

            self.producer.send(
                "bank.merchants",
                merchant["merchant_id"],
                merchant
            )

            self.merchant_counter += 1

    # -----------------------------
    # RUN BATCH
    # -----------------------------
    def run_batch(self, new_customers=5, accounts_per_customer=2, txns_per_account=10):

        print(f"\n--- Batch Started {datetime.utcnow()} ---")

        self.init_merchants()

        # =========================
        # CUSTOMERS (STATEFUL)
        # =========================
        for _ in range(new_customers):

            customer = generate_customer(self.customer_counter)

            customer = self.state.upsert_customer(customer)

            # occasional update
            if random.random() < 0.2:
                customer["last_name"] = customer["last_name"] + "_UPD"

            self.producer.send(
                "bank.customers",
                customer["customer_id"],
                customer
            )

            # =========================
            # LOAN
            # =========================
            loan = generate_loan(customer["customer_id"], self.loan_counter)

            self.state.add_loan(loan)

            self.producer.send(
                "bank.loans",
                loan["loan_id"],
                loan
            )

            self.loan_counter += 1

            # =========================
            # ACCOUNTS
            # =========================
            accounts = generate_accounts(
                customer["customer_id"],
                self.account_counter,
                accounts_per_customer
            )

            for acc in accounts:

                self.state.add_account(acc)

                self.producer.send(
                    "bank.accounts",
                    acc["account_id"],
                    acc
                )

                # =========================
                # CARD
                # =========================
                card = generate_card(
                    customer["customer_id"],
                    acc["account_id"],
                    self.card_counter
                )

                self.state.add_card(card)

                # occasional update
                if random.random() < 0.1:
                    card["status"] = "BLOCKED"

                self.producer.send(
                    "bank.cards",
                    card["card_id"],
                    card
                )

                self.card_counter += 1

                # =========================
                # EVENT
                # =========================
                event = generate_account_event(
                    acc["account_id"],
                    customer["customer_id"]
                )

                self.producer.send(
                    "bank.account_events",
                    event["event_id"],
                    event
                )

                # =========================
                # TRANSACTIONS (ONLY ACTIVE ACCOUNTS)
                # =========================
                if acc["status"] != "CLOSED":

                    txns = generate_transactions(
                        account=acc,
                        customer_id=customer["customer_id"],
                        txn_start_id=self.transaction_counter,
                        num_txns=txns_per_account,
                        base_date=datetime.utcnow()
                    )

                    for txn in txns:

                        # inject AML fraud
                        if random.random() < 0.05:
                            txn["amount"] = random.uniform(10000, 20000)
                            txn["merchant"] = "CRYPTO_EXCHANGE"
                            txn["flag"] = "SUSPICIOUS"

                        self.producer.send(
                            "bank.transactions",
                            txn["transaction_id"],
                            txn
                        )

                    self.transaction_counter += txns_per_account

                self.account_counter += 1

            self.customer_counter += 1

        self.producer.flush()

        print("--- Batch Completed ---\n")