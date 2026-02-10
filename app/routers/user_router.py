from sqlmodel import Session
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.user_service import update_user
from app.schemas.user_schema import SingleUserResponse, UserUpdate
from app.databases.session import get_session

router = APIRouter(prefix="/users", tags=["user"])

@router.patch("/{id}", response_model=SingleUserResponse)
def update_user_endpoint(
    id: int,
    name: str | None,
    email: str | None,
    password: str | None,
    session: Session =  Depends(get_session)
):
    try:
        data_dict = UserUpdate(
            name=name,
            email=email,
            password=password
        )
        
        updated = update_user(
            session=session,
            id=id,
            data=data_dict
        )
        
        if not updated:
            raise HTTPException(404, "User is not found")
        
        return {
            "status": "Success",
            "message": "User successfully updated",
            "data": updated
        }
    except Exception as e:
        raise HTTPException(400, str(e))