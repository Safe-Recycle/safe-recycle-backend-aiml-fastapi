from sqlmodel import Session, select, func
from typing import Optional
from datetime import datetime, timezone

from app.core.sequrity import get_password_hashed, verify_password
from app.models.user_model import User
from app.schemas.user_schema import UserUpdate

def show_user(
    session: Session,
    limit: int,
    offset: int,
    name: Optional[str] = None
):
    statement = select(User)
    
    if name: 
        statement = statement.where(
            User.name.ilike(f"%{name}%")
        )
        
    total = session.exec(
        select(func.count()).select_from(statement.subquery())
    ).one()
    
    items = session.exec(
        statement.offset(offset).limit(limit)
    )
    
    return items, total

def update_user(
    session: Session, 
    id: int,
    data: UserUpdate
):
    existing = session.exec(
        select(User).where(User.id == id)
    ).first()
    
    if not existing:
        raise ValueError("NOT_FOUND")
    
    if data.email:
        email = session.exec(
            select(User).where(User.email == data.email)
        ).first()
                
        if email:
            raise ValueError("EMAIL_USED")
        
    if data.password:
        user = session.exec(
            select(User).where(User.id == id)
        ).first()
        
        if  not verify_password(data.old_password, user.hashed_password): 
            raise ValueError("PASSWORD_WRONG")
        if data.password != data.password_confirm:
            raise ValueError("PASSWORD_NOT_MATCHED")
        
        hashed_password = get_password_hashed(data.password)
        
    updated_data = data.model_dump(exclude_unset=True)
    updated_data.pop("old_password", None)
    updated_data.pop("password_confirm", None)
    updated_data.pop("password", None)
    
    for field, value in updated_data.items():
        setattr(existing, field, value)
    
    existing.hashed_password = hashed_password     
    existing.updated_at = datetime.now(timezone.utc)
    
    session.add(existing)
    session.commit()
    session.refresh(existing)
    
    return existing

def delete_user(
    session: Session,
    id: int
):
    existing = session.exec(
        select(User).where(User.id == id)
    ).first()
    
    if not existing:
        raise ValueError("NOT_FOUND")
    
    if existing.disabled:
        raise ValueError("ALREADY_DISABLED")
    
    existing.disabled = True
    existing.updated_at = datetime.now(timezone.utc)
    
    session.add(existing)
    session.commit()
    session.refresh(existing)
    
    return existing