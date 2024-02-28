from fastapi import FastAPI

from maxcom.router import router as maxcom_router
from pcmarket.router import router as pcmarket_router
from ikarvon.router import router as ikarvon_router

MAIN_URL = '/api/v1/'

urls = [
    ('parse-maxcom', maxcom_router),
    ('parse-pcmarket', pcmarket_router),
    ('parse-ikarvon', ikarvon_router)
]


def init_router(app: FastAPI):
    for url, router in urls:
        app.include_router(router, prefix=f'{MAIN_URL}{url}')
