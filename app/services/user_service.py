from sqlmodel import Session, select
from typing import Optional
from datetime import datetime, timezone

from app.core.sequrity import get_password_hashed
from app.models.user_model import User
from app.schemas.user_schema import UserRead, UserUpdate

def update_user(
    session: Session, 
    id: int,
    data: UserUpdate
):
    existing = session.exec(
        select(User).where(User.id == id)
    ).first()
    
    if not existing:
        raise ValueError("User is not exist")
    
    if data.email:
        email = session.exec(
            select(User).where(User.email == data.email)
        ).first
        
        if email:
            raise ValueError("Email is already used")
        
    if data.password:
        data.password = get_password_hashed(data.password)
        
    updated_data = data.model_dump(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(existing, field, value)
        
    existing.updated_at = datetime.now(timezone.utc)
    
    session.add(existing)
    session.commit()
    session.refresh(existing)
    
    return existing