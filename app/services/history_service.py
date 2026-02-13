from sqlmodel import Session, func, select
from typing import Optional, List
from datetime import datetime, timezone

from app.models.history_model import History
from app.schemas.history_schema import CreateHistory

def create_history(session: Session, data: CreateHistory):   
    history = History(
        user_id=data.user_id,
        item_id=data.item_id
    ) 
    
    session.add(history)
    session.commit()