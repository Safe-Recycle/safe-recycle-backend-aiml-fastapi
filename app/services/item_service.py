from sqlmodel import Session, func, select
from typing import Optional, List
from datetime import datetime, timezone 

from app.models.item_model import Item
from app.models.category_model import Category
from app.schemas.item_schema import CreateItem, ReadItem, UpdateItem, ShowItem

def create_item(session: Session, data: CreateItem) -> ReadItem:
    existing = session.exec(
        select(Item).where(Item.name == data.name)
    ).first()
    
    if existing:
        raise ValueError("Item is already exist")
    
    category = session.exec(
        select(Category).where(Category.name == data.category_name)
    ).first()
    
    if category is None:
        raise ValueError("Category name is not available")
    
    item = Item(
        name=data.name,
        image_link=data.image_link,
        description=data.description,
        recycle=data.recycle,
        is_reusable=data.is_reusable,
        is_recyclable=data.is_recyclable,
        is_hazardous=data.is_hazardous,
        category_id=category.id
    )
    
    session.add(item)
    session.commit()
    session.refresh(item)
    
    return item    

def read_item(session: Session, id: int) -> ReadItem | None:
    item = session.exec(
        select(Item).where(Item.id == id)
    ).first()
    
    return item

def show_item(
    session: Session, 
    limit: int,
    offset: int,
    name: Optional[str] = None, 
    category: Optional[int] = None,
):
    statement = select(Item)
    
    if name:
        statement = statement.where(
            Item.name.ilike(f"%{name}%")
        )
        
    if category:
        statement = statement.where(
            Item.category_id == category
        )
        
    total = session.exec(
        select(func.count()).select_from(statement.subquery())
    ).one()
    
    items = session.exec(
        statement.offset(offset).limit(limit)
    ).all()
    
    return items, total

def update_item(session: Session, id: int, data: UpdateItem):
    existing = session.exec(
        select(Item).where(Item.id == id)
    ).first()
    
    if not existing:
        raise ValueError("Item is not exist")
    
    if data.category_name:
        category = session.exec(
            select(Category).where(Category.name == data.category_name)
        ).first()
        
        if not category:
            raise ValueError("Category is not exist")

        existing.category_id = category.id
    
    updated_data = data.model_dump(exclude_unset=True)
    updated_data.pop("category_name", None)
    
    for field, value, in updated_data.items():
        setattr(existing, field, value)
        
    existing.updated_at = datetime.now(timezone.utc)
    
    session.add(existing)
    session.commit()
    session.refresh(existing)
            
    return existing

def delete_item(
    session: Session,
    id: int
):
    item = session.exec(
        select(Item).where(Item.id == id)
    ).first()
    
    if not item:
        return None
    
    session.delete(item)
    session.commit()
    
    return item