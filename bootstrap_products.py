from data_generator.generators.product_generator import generate_product_by_type
from data_generator.generators.merchant_generator import generate_merchant
from data_generator.producers.kafka_producer import KafkaProducerClient


def bootstrap_products():

    producer = KafkaProducerClient()

    print("Bootstrapping PRODUCTS (one-time setup)...")

    product_types = ["CHECKING", "SAVINGS", "CREDIT_CARD", "LOAN"]

    product_id = 1

    for ptype in product_types:

        product = generate_product_by_type(ptype)

        product_record = {

            "product_id": f"P{product_id:03d}",

            "product_type": ptype,

            "product_code": product["product_code"],

            "product_name": product["product_name"],

            "risk_level": product["risk_level"]
        }

        producer.send(
            topic="bank.products",
            key=product_record["product_id"],
            value=product_record
        )

        print(f"Sent product: {product_record}")

        product_id += 1

    producer.flush()

    print("PRODUCT BOOTSTRAP COMPLETE")


if __name__ == "__main__":

    bootstrap_products()