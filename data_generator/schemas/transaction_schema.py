TRANSACTION_SCHEMA = {
    "transaction_id": str,
    "account_id": str,
    "customer_id": str,
    "transaction_type": str,
    "amount": float,
    "currency": str,
    "merchant": str,
    "channel": str,
    "transaction_date": str,
    "location": str,
    "is_suspicious": bool,
    "risk_score": float
}