import traceback

from typing import List, Annotated
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException

from app.models.user_model import User
from app.schemas.history_schema import PopularItem, ResponsePopularItem, ResponseRecommendations
from app.databases.session import get_session
from app.services.history_service import get_popular_items, get_recommendations
from app.services.authentication_service import get_current_active_user

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/popular", response_model=ResponsePopularItem)
def popular_items(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    try:
        items = get_popular_items(session)

        clean_items = [PopularItem.model_validate(item) for item in items]

        response = {
            "status": "success",
            "message": "Popular items fetched successfully",
            "data": clean_items
        }

        return response

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Error fetching popular items: {str(e)}")

@router.get("/recommendation/{id}")
def get_recommendation_endpoint(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session)
):
    if current_user.id != id:
        HTTPException(403, "You are not authenticated with this id")
    
    recommendations = get_recommendations(
        session=session,
        user_id=id
    )
    
    return ResponseRecommendations(
        status="success",
        message="Recommendations fetched successfully",
        data=recommendations
    )