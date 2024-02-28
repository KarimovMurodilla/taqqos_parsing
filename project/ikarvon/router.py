from fastapi import APIRouter

from ikarvon.category import parse_category
from ikarvon.product import parse_product
from services import get_all_categories

router = APIRouter()


@router.get('/category')
def parse_category_ikarvon():
    parse_category.delay()
    return {"detail": "Ok"}


@router.get('/product')
def parse_product_ikarvon():
    data = [category.url for category in get_all_categories(website="ikarvon")]
    parse_product.delay(data)
    return {"detail": "Ok"}
