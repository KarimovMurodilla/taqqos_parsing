from sqlalchemy import Column, Integer, String

from db.database import Base


class Category(Base):
    __tablename__ = "texnomart_category"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
