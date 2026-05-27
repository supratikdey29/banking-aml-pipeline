import json
import os


class StateStore:

    def __init__(self, base_path="data_generator/state"):

        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

        # -----------------------------
        # IN-MEMORY STATE
        # -----------------------------
        self.customers = {}
        self.accounts = {}
        self.cards = {}
        self.loans = {}
        self.merchants = {}

        self.counters = {
            "customer": 1,
            "account": 1,
            "card": 1,
            "loan": 1,
            "merchant": 1,
            "transaction": 1
        }

        # load existing state if available
        self.load_state()

    # =====================================================
    # FILE HELPERS
    # =====================================================
    def _path(self, name):
        return os.path.join(self.base_path, f"{name}.json")

    def save_state(self):

        state = {
            "customers": self.customers,
            "accounts": self.accounts,
            "cards": self.cards,
            "loans": self.loans,
            "merchants": self.merchants,
            "counters": self.counters
        }

        for k, v in state.items():

            with open(self._path(k), "w") as f:
                json.dump(v, f, indent=2, default=str)

    def load_state(self):

        for name in ["customers", "accounts", "cards", "loans", "merchants", "counters"]:

            try:
                with open(self._path(name), "r") as f:
                    setattr(self, name, json.load(f))
            except:
                pass

    # =====================================================
    # CUSTOMER
    # =====================================================
    def upsert_customer(self, customer):

        cid = customer["customer_id"]

        if cid not in self.customers:
            self.customers[cid] = customer
        else:
            self.customers[cid].update(customer)

        self.save_state()
        return self.customers[cid]

    # =====================================================
    # ACCOUNT
    # =====================================================
    def add_account(self, account):

        self.accounts[account["account_id"]] = account
        self.save_state()
        return account

    def update_account(self, account_id, updates):

        if account_id in self.accounts:
            self.accounts[account_id].update(updates)

        self.save_state()
        return self.accounts.get(account_id)

    # =====================================================
    # CARD
    # =====================================================
    def add_card(self, card):

        self.cards[card["card_id"]] = card
        self.save_state()
        return card

    def update_card(self, card_id, updates):

        if card_id in self.cards:
            self.cards[card_id].update(updates)

        self.save_state()
        return self.cards.get(card_id)

    # =====================================================
    # LOAN
    # =====================================================
    def add_loan(self, loan):

        self.loans[loan["loan_id"]] = loan
        self.save_state()
        return loan

    def update_loan(self, loan_id, updates):

        if loan_id in self.loans:
            self.loans[loan_id].update(updates)

        self.save_state()
        return self.loans.get(loan_id)

    # =====================================================
    # MERCHANT
    # =====================================================
    def add_merchant(self, merchant):

        self.merchants[merchant["merchant_id"]] = merchant
        self.save_state()
        return merchant

    # =====================================================
    # COUNTERS
    # =====================================================
    def next_id(self, key):

        value = self.counters.get(key, 1)
        self.counters[key] = value + 1
        self.save_state()
        return value