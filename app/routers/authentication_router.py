from fastapi import Depends, APIRouter, HTTPException, status, Header
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.databases.session import get_session
from app.models.user_model import User
from app.schemas.token_schema import TokenRequest
from app.schemas.user_schema import UserCreate, UserRead
from app.services.authentication_service import authenticate_user, create_access_token, create_user, get_current_active_user, create_refresh_token, logout_user, revoke_refresh_token, validate_refresh_token
from app.schemas.token_schema import Token
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
) -> Token:
    user = authenticate_user(session, form_data.username.lower(), form_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        user_id=user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        session, user.id
    )
    
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer"
    )
    
@router.get("/users/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.name}]

@router.post("/register", response_model=UserRead, status_code=201)
def register(user_in: UserCreate, session: Session = Depends(get_session)):
    try:
        return create_user(session, user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.post("/refresh")
def refresh_access_token(
    data: TokenRequest,
    session: Session = Depends(get_session)
):
    try:
        # 1. Validate refresh token
        refresh_token = validate_refresh_token(session, data.refresh_token)
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        user_id = refresh_token.user_id

        # 2. Revoke old refresh token (rotation)
        revoke_refresh_token(session=session, refresh_token=refresh_token)

        # 3. Create new tokens
        access_token = create_access_token(user_id=user_id)
        new_refresh_token = create_refresh_token(session, user_id)

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    except HTTPException:
        # biarin HTTPException lewat (401, 403, dll)
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while refreshing token"
        )
        
@router.post("/logout")
def logout(
    data: TokenRequest,
    authorization: str = Header(...),
    session: Session = Depends(get_session)
):
    token = authorization.replace("Bearer ", "")
    logout_user(session, token)
    refresh = validate_refresh_token(session=session, token=data.refresh_token)
    
    if refresh:
        revoke_refresh_token(session, refresh)
    return {"message": "Logout successful"}