def generate_product_by_type(product_type):

    products = {

        "CHECKING": {
            "product_code": "CHK_STD",
            "product_name": "Standard Checking Account",
            "risk_level": "LOW"
        },

        "SAVINGS": {
            "product_code": "SAV_STD",
            "product_name": "Standard Savings Account",
            "risk_level": "LOW"
        },

        "CREDIT_CARD": {
            "product_code": "CC_PREM",
            "product_name": "Premium Credit Card",
            "risk_level": "MEDIUM"
        },

        "LOAN": {
            "product_code": "LN_PERSONAL",
            "product_name": "Personal Loan",
            "risk_level": "HIGH"
        }
    }

    return products.get(product_type, products["CHECKING"])