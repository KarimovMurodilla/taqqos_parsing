from fastapi import FastAPI

MAIN_URL = '/api/v1//'

urls = [
]


def init_router(app: FastAPI):
    for url, router in urls:
        app.include_router(prefix=f'{MAIN_URL}{url}', router=router)
