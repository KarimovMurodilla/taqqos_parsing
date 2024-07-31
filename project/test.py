
# from pcmarket.category import parse_category
# from pcmarket.product import parse_product

from mediapark.category import prog as mediapark_category
from mediapark.product import prog as mediapark_product

from services import get_all_categories


if __name__ == '__main__':
    mediapark_category()

    data = [category.url for category in get_all_categories(website="mediapark")]

    # mediapark_product(data)
