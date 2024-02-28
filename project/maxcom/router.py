from fastapi import APIRouter

from maxcom.product import category_parse

router = APIRouter()


@router.get('/')
def category_parse_maxcom():
    category_parse.delay()
    return {"detail": "ok"}
