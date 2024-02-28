from fastapi import APIRouter

from pcmarket.category import parse_category as pcmarket_category
from pcmarket.product import parse_product as pcmarket_product
from services import get_all_categories

router = APIRouter()


@router.get('/category')
def pcmarket_parse_category():
    pcmarket_category()
    return {"detail": "Ok"}


@router.get('/product')
def pcmarket_parse_product():
    data = [category.url for category in get_all_categories(website="pcmarket")]
    pcmarket_product(data)
    return {"detail": "Ok"}
