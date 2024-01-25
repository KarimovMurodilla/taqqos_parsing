from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def database_connect(func):
    def connect(*args, **kwargs):
        session = SessionLocal()
        try:
            return func(session=session, *args, **kwargs)
        finally:
            session.close()

    return connect
