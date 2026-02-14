from sqlmodel import Session, func, select
from typing import Optional, List
from datetime import datetime, timezone
from collections import defaultdict
import math

from app.models.history_model import History
from app.models.item_model import Item
from app.schemas.history_schema import CreateHistory, Recommendations

def create_history(session: Session, data: CreateHistory):   
    history = History(
        user_id=data.user_id,
        item_id=data.item_id
    ) 
    
    session.add(history)
    session.commit()
    
def collaborative_filtering(session: Session, user_id: int, top_k: int = 6):    
    histories = session.exec(
        select(History)
    ).all()
    
    user_items = defaultdict(set)
    for h in histories:
        user_items[h.user_id].add(h.item_id)
        
    if user_id not in user_items:
        return []
    
    target_items = user_items[user_id]
    
    similarity_scores = {}
    for other_users, items in user_items.items():
        if other_users == user_id:
            continue
        
        intersections = len(target_items & items)
        norm = math.sqrt(len(target_items)) * math.sqrt(len(items))
        
        if norm == 0:
            continue
        
        similarity_scores[other_users] = intersections / norm
        
    similar_users = sorted(
        similarity_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]
    
    recommended = set()
    for other_user, _ in similar_users:
        recommended.update(user_items[other_user])
        
    return list(recommended - target_items)
    
def get_recommendations(session: Session, user_id: int) -> List | None:
    MIN_USERS = 3
    MIN_INTERACTIONS = 20
    
    total_users = session.exec(
        select(func.count(func.distinct(History.user_id)))
    ).one()
    
    total_interactions = session.exec(
        select(func.count()).select_from(History)
    ).one()
    
    user_history = session.exec(
        select(History).where(History.user_id == user_id)
    ).all()
    
    if total_users < MIN_USERS or total_interactions < MIN_INTERACTIONS:
        return []
    
    if not user_history:
        return []
    
    similarities = collaborative_filtering(session=session, user_id=user_id)

    items = session.exec(
        select(Item).where(Item.id.in_(similarities))
    ).all()
    
    item_map = {item.id: item for item in items}
    
    recommendations = [
        Recommendations(
            item_id=item_id,
            item_name=item_map[item_id].name
        )
        for item_id in similarities
        if item_id in item_map
    ]
        
    return recommendations