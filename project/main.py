from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urls import init_router


def get_app():
    app = FastAPI(debug=True)
    init_router(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = get_app()
