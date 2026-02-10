from sqlmodel import Session
from typing import Optional
import math
from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.user_service import show_user, update_user, delete_user
from app.schemas.user_schema import SingleUserResponse, UserUpdate, SingleUserDeleteResponse, UserListResponse
from app.databases.session import get_session

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/", response_model=UserListResponse)
def show_user_endpoint(
    name: Optional[str] = Query(
        default=None,
        description="Search user by name"
    ),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=10),
    session: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    
    users, total = show_user(
        session=session,
        name=name,
        limit=limit,
        offset=offset
    )
    
    total_pages = math.ceil(total / limit)
    
    return {
        "status": "success",
        "message": "Users fetched successfully",
        "data": users,
        "meta": {
            "page": page,
            "limit": limit,
            "total_items": total,
            "total_pages": total_pages
        }
    }

@router.patch("/{id}", response_model=SingleUserResponse)
def update_user_endpoint(
    id: int,
    data: UserUpdate,
    session: Session =  Depends(get_session)
):
    try:
        updated = update_user(
            session=session,
            id=id,
            data=data
        )
        
        if not updated:
            raise HTTPException(404, "User is not found")
        
        return {
            "status": "Success",
            "message": "User successfully updated",
            "data": updated
        }
    except Exception as e:
        if str(e) == "NOT_FOUND":
            raise HTTPException(404, "User is not found")
        elif str(e) == "EMAIL_USED":
            raise HTTPException(400, "Email is already used")
        elif str(e) == "PASSWORD_WRONG":
            raise HTTPException(400, "Your password is wrong")
        elif str(e) == "PASSWORD_NOT_MATCHED":
            raise HTTPException(400, "Password and confirm password is not matched")
        else:
            raise HTTPException(400, str(e))
    
@router.patch("/delete-soft/{id}", response_model=SingleUserDeleteResponse)
def delete_user_endpoint(
    id: int,
    session: Session = Depends(get_session)
):
    try:
        deleted = delete_user(session=session, id=id)
        
        return {
            "status": "Success",
            "message": f"User {id} is successfully deleted softly",
            "data": deleted
        }
    except Exception as e:
        if str(e) == "NOT_FOUND":
            raise HTTPException(404, "User not found")
        elif str(e) == "ALREADY_DISABLED":
            raise HTTPException(400, "User already disabled")
        else:
            raise HTTPException(400, str(e))