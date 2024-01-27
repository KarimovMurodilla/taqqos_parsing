from sqlalchemy.orm import Session
from db.get_db import database_connect
from models.category import Category
from schemas import CategorySchema


@database_connect
def create_category(db: Session, data: CategorySchema) -> None:
    category = db.query(Category).filter(Category.name == data.name).first()
    if category is None:
        category = Category(**data.dict())
        db.add(category)
    else:
        category.name = data.name
    db.commit()


@database_connect
def get_all_categories(db: Session):
    categories = db.query(Category)
    return categories
