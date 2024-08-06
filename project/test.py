
# from pcmarket.category import parse_category
# from pcmarket.product import parse_product

from olcha.category import prog as olcha_category
from olcha.product import prog as olcha_product

from services import get_all_categories


if __name__ == '__main__':
    # olcha_category()

    data = [category.url for category in get_all_categories(website="olcha")]

    olcha_product(data)
