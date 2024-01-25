from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def database_connect(func):
    def connect(*args, **kwargs):
        db = SessionLocal()
        try:
            return func(db=db, *args, **kwargs)
        finally:
            db.close()

    return connect
