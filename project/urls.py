from fastapi import FastAPI

from parser_runners import router as parser_router

MAIN_URL = '/api/v1/'

urls = [
    ('parse-maxcom', parser_router)
]


def init_router(app: FastAPI):
    for url, router in urls:
        app.include_router(router, prefix=f'{MAIN_URL}{url}')
