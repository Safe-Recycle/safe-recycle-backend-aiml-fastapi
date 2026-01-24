from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.category_service import read_category, show_category, create_category
from app.databases.session import get_session
from app.schemas.category_schema import ReadCategory, CreateCategory

router = APIRouter(prefix="/api/categories", tags=["category"])

@router.get("/{id}")
def read_category_endpoint(id: int, session: Session = Depends(get_session)):
    category = read_category(session, id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category

@router.get("/", response_model = List(ReadCategory))
def show_categories_endpoint(
    name: Optional[str] = Query(
        default=None,
        description="Search category by name"
    ),
    session: Session = Depends(get_session)
):
    return show_category(session=session, name=name)

@router.post("/", response_model=ReadCategory, status_code=201)
def create_category_endpoint(data: CreateCategory, session: Session = Depends(get_session)):
    try:
        return create_category(data=data, session=session)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
