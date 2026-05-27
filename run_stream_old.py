from data_generator.producers.stream_runner import BankingStreamRunner

runner = BankingStreamRunner()

# SIMULATE DAILY RUN
runner.run_batch(
    new_customers=5,
    accounts_per_customer=2,
    txns_per_account=10
)