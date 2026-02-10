from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
import secrets
import hashlib

from app.core.sequrity import get_password_hashed, get_user_by_email, verify_password
from app.core.config import settings
from app.databases.session import get_session
from app.models.refresh_token_model import RefreshToken
from app.models.token_blockedlist import TokenBlockedList
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_HOURS = 3

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ==================== Login Account ====================    
def authenticate_user(session: Session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return user

def create_access_token(
    user_id: int, 
    expires_delta: timedelta | None = None
):
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "jti": secrets.token_hex(16)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)], 
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        jti = payload.get("jti")
        if user_id is None or jti is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    # Checking access token in blacklist
    blocked = session.exec(
        select(TokenBlockedList).where(TokenBlockedList.jti == jti)
    ).first()   
    if blocked:
        raise credentials_exception
    
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

# ==================== Register Account ====================
def create_user(session: Session, user_in: UserCreate) -> User:
    existing_user = session.exec(
        select(User).where(User.name == user_in.name)
    ).first()
    
    if existing_user:
        raise ValueError("Username already exist")
    
    existing_email = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    
    if existing_email:
        raise ValueError("Email is already used")
    
    user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hashed(user_in.password)
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ==================== Refresh Token ====================
def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def create_refresh_token(session: Session, user_id: int) -> str:
    raw_token = secrets.token_urlsafe(32)
    token_hash = _hash_token(raw_token)
    
    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    )
    
    session.add(refresh_token)
    session.commit()
    
    return raw_token

def validate_refresh_token(session: Session, token: str) -> RefreshToken | None:
    token_hash = _hash_token(token)
    
    refresh_token = session.exec(
        select(RefreshToken).where(
            RefreshToken.token_hash==token_hash,
            RefreshToken.revoked == False
        )
    ).first()
    
    if not refresh_token:
        return None
    
    if refresh_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return None
    
    return refresh_token

def revoke_refresh_token(session: Session, refresh_token: RefreshToken):
    refresh_token.revoked = True
    session.add(refresh_token)
    session.commit()
    
# ==================== Logout Account ====================
def logout_user(session: Session, token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Blacklist Access Token
    jti = payload.get("jti")
    exp = payload.get("exp")
    
    expired = datetime.fromtimestamp(exp, tz=timezone.utc)
    
    blacklist = TokenBlockedList(
        jti=jti,
        expired_at=expired
    )
        
    session.add(blacklist)    
    session.commit()