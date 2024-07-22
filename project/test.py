
# from pcmarket.category import parse_category
# from pcmarket.product import parse_product

from asaxiy.category import prog as asaxiy_category
from asaxiy.product import prog as asaxiy_product

from services import get_all_categories


if __name__ == '__main__':
    # asaxiy_category()

    data = [category.url for category in get_all_categories(website="asaxiy")]

    asaxiy_product(data)
