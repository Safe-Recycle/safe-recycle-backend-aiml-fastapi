from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timezone 

from app.models.category_model import Category
from app.schemas.category_schema import CreateCategory

def read_category(session: Session, id: int) -> Category | None:
    category = session.exec(
        select(Category).where(Category.id == id)        
    ).first()
    
    return category

def show_category(session: Session, name: Optional[str]):
    statement = select(Category)
    
    if name:
        statement = statement.where(
            Category.name.ilike(f"%{name}%")
        )
    
    return session.exec(statement).all()

def create_category(session: Session, data: CreateCategory) -> Category:
    existing = session.exec(
        select(Category).where(Category.name == data.name)
    ).first()
    
    if existing:
        raise ValueError("Category already exist")
    
    category = Category(
        name=data.name,
        image_link=data.image_link
    )
    
    session.add(category)
    session.commit()
    session.refresh(category)
    
    return category

def update_category(
    session: Session, 
    id: int,
    name: str | None = None,
    image_link: str | None = None 
) -> Category | None:
    category = session.exec(
        select(Category).where(Category.id == id)
    ).first()
    
    if not category: 
        return None
    
    if name is not None:
        category.name = name
    
    if image_link is not None:
        category.image_link = image_link
        
    category.updated_at = datetime.now(timezone.utc)

    session.add(category)
    session.commit()
    session.refresh(category)

    return category

def delete_cetegory(
    session: Session,
    id: int
):
    category = session.exec(
        select(Category).where(Category.id == id)
    ).first()
    
    if not category:
        return None
    
    session.delete(category)
    session.commit()
    
    return category