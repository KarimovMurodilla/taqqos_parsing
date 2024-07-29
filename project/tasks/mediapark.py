from services import get_all_categories

from mediapark.category import prog as mediapark_category
from mediapark.product import prog as mediapark_product


def parse_mediapark_category():
    try:
        mediapark_category()
    except Exception as e:
        print(f"Error in parse_mediapark_category: {e}")


def parse_mediapark_product():
    try:
        data = [category.url for category in get_all_categories(website="mediapark")]
        if not data:
            parse_mediapark_category() 
        mediapark_product(data)
    except Exception as e:
        print(f"Error in parse_mediapark_product: {e}")
