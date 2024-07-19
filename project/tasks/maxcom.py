from maxcom.product import category_parse as maxcom_parse


def parse_maxcom_product():
    try:
        maxcom_parse()
    except Exception as e:
        print(f"Error in parse_maxcom_product: {e}")

