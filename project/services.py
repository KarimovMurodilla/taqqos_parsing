from sqlalchemy.orm import Session
from db.get_db import database_connect
from models.category import Category
from schemas import CategorySchema


@database_connect
def create_category(db: Session, data: CategorySchema) -> None:
    category = db.query(Category).filter((Category.name == data.name) & (Category.url == data.url)).first()
    if category is None:
        category = Category(**data.dict())
        db.add(category)
    else:
        category.name = data.name
    db.commit()


@database_connect
def get_all_categories(db: Session, website: str):
    categories = db.query(Category).filter(Category.website == website)
    return categories
