from fastapi import APIRouter

from maxcom.product import category_parse as maxcom_parser

router = APIRouter()


@router.get('/')
def parse_maxcom():
    maxcom_parser.delay()
    return {"detail": "ok"}